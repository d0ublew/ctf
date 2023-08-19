#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import base64

from pwn import *

# nc cryptic.sibersiaga2023.myctf.io 9999
io = remote('cryptic.sibersiaga2023.myctf.io', 9999)

i = 0
while True:
    try:
        io.recvuntil(b"Decrypt and solve: ")
    except EOFError:
        io.interactive()
    raw_q = io.recvline(keepends=False).decode().split(" ")
    print(raw_q)
    log.info(raw_q[0])
    possible = []
    possible.append(base64.b64decode(eval(raw_q[0])))
    print(possible)
