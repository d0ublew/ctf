#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./dist/heapheapheap", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
"""


def add(s, v):
    io.sendlineafter(b"Your choice: ", b"1")
    io.sendlineafter(b"Enter length", str(len(s) + 1).encode())
    io.sendlineafter(b"Enter string: ", s)
    io.sendlineafter(b"Enter value: ", str(v).encode())


def delete():
    io.sendlineafter(b"Your choice: ", b"3")
    io.recvuntil(b"The largest element is '")
    string = io.recvuntil(b"'")[:-1]
    io.recvuntil(b"with a value of ")
    return string, int(io.recvline())


io = start()

io.interactive()
