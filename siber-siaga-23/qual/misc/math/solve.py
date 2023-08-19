#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import math
import re
import statistics

from pwn import *

io = remote('math.sibersiaga2023.myctf.io', 8887)

i = 0
while True:
    try:
        io.recvuntil(b"Find")
    except EOFError:
        io.interactive()
    raw_q = io.recvline(keepends=False).decode()
    log.info(raw_q)
    if "Average" in raw_q:
        lst = eval(re.search(r'\[.+\]', raw_q)[0])
        io.sendline(str(sum(lst) / len(lst)).encode())
    elif "Median" in raw_q:
        lst = eval(re.search(r'\[.+\]', raw_q)[0])
        io.sendline(str(statistics.median(lst)).encode())
    elif "mod" in raw_q:
        eq = re.search(r'\[.+\]', raw_q)[0][1:-1].split(" mod ")
        res = int(eq[0]) % int(eq[1])
        io.sendline(str(res).encode())
    elif "Min" in raw_q:
        lst = eval(re.search(r'\[.+\]', raw_q)[0])
        io.sendline(str(min(lst)).encode())
    elif "Max" in raw_q:
        lst = eval(re.search(r'\[.+\]', raw_q)[0])
        io.sendline(str(max(lst)).encode())
    else:
        io.interactive()
    i += 1
    if i == 100:
        print(io.recvall(timeout=1))
        io.interactive()
