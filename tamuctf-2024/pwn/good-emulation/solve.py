#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = ELF("./good-emulation")

io = remote("localhost", 9001)

io.recvline()
maps = io.recvuntil(b"buf is at ", drop=True).decode().split("\n")
print(maps)
leak_buf = int(io.recvline(), 16)
log.info(f"{leak_buf=:#x}")

io.interactive()
