#!/usr/bin/env python3

from pwn import *
import re


def next_num(a, b, seed):
    return (b + a * seed) & 0xffff


def parse_num(s):
    s = s.replace(b"\x1b[", b"#").strip()
    return int(re.search(rb"#.+m\$?(\d+)#.+m", s).group(1))


def bet(n):
    io.sendlineafter(b">>> ", str(n).encode("utf-8"))


def guess(n):
    io.sendlineafter(b">>> ", str(n).encode("utf-8"))


io = process("./lucky")
# io = remote("puzzler7.imaginaryctf.org", 11001)

bet(5)
b = parse_num(io.recvline())
log.info(f"{b=}")

guess(1)

seed = parse_num(io.recvline())

'''
intended way to find `a`
math:
x2 = a*x1 + b
x3 = a*x2 + b

b = x3 - a*x2
x2 = a*x1 + x3 - a*x2
a = (x2 - x3)/(x1 - x2)
'''

a = None
for i in range(1, 0x10000):
    if (b + i * b) & 0xffff == seed:
        a = i
        break

log.info(f"{a=}")

io.recvline()
io.recvline()
money = parse_num(io.recvline())

while money <= 1000000000:
    bet(money)
    first_seed = parse_num(io.recvline())
    next_number = next_num(a, b, first_seed)
    guess(int(next_number < first_seed) + 1)
    second_number = io.recvline()
    io.recvline()
    io.recvline()
    money = parse_num(io.recvline())

io.interactive()
