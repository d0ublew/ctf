#!/usr/bin/env python3

from pwn import *
import re


def parse_regex(rg):
    tokens = re.findall(rb'\[(\w+)\](\{\d+\})?', rg)
    return tokens


def gen_string(rg):
    tokens = parse_regex(rg)
    string = b""
    for token in tokens:
        alpha, qty = token
        if len(qty) > 0:
            qty = int(qty[1:-1])
        else:
            qty = 1
        string += bytes([alpha[0]]) * qty
    return string


io = remote("puzzler7.imaginaryctf.org", 11003)

solved = 0

while solved < 100:
    print(solved)
    io.recvuntil(b"regex:\n", drop=True)
    rg = io.recvline().strip()
    io.sendlineafter(b">>> ", gen_string(rg))
    solved += 1

io.interactive()
