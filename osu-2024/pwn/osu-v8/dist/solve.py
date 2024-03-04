#!/usr/bin/env python3

from pwn import *

with open("./pwn.js", "rb") as f:
    payload = f.read()

io = remote("chal2.osugaming.lol", 7000)

io.sendline(str(len(payload)).encode())
io.send(payload)

io.clean()
io.interactive()
