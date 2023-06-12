#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *
import string
import sys

elf = context.binary = ELF("./dist/chall")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port, timeout=10)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}


def create():
    io.sendafter(b"> ", b"1")


def write(idx: int, size: int, content: bytes):
    io.sendafter(b"> ", b"2")
    io.sendlineafter(b"idx = ", str(idx).encode("utf-8"))
    io.sendlineafter(b"write = ", str(size).encode("utf-8"))
    io.send(content)


def read(idx: int):
    io.sendafter(b"> ", b"3")
    io.sendafter(b"idx = ", str(idx).encode("utf-8"))


io = start()

pause()
for i in range(100):
    create()
    write(i, i, b"A" * i)

io.interactive()
