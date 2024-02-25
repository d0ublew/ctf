#!/usr/bin/env python3


import base64

from pwn import *

with open("./input.rom", "rb") as f:
    input_rom = base64.b64encode(f.read())

nc = "nc mc.ax 31442"
nc = nc.split()
io = remote(nc[1], nc[2])
io.sendline(input_rom)
io.interactive()
