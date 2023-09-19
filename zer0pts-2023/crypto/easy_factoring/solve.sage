#!/usr/bin/env sage

from pwn import *

io = remote("crypto.2023.zer0pts.com", int(10333))

io.recvline()

N = int(io.recvline().decode().split(" ")[-1])
log.info(f"{N=}")

p, q = sum_of_k_squares(2, N)

io.sendline(str(p).encode())
io.sendline(str(q).encode())
io.interactive()
