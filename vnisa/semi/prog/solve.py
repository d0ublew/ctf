#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from decimal import *
from math import gcd

from pwn import *
from sympy.ntheory.factor_ import totient

# def find_period_of_repeating_decimal(denominator):
#     if gcd(10, denominator) != 1:
# return "The denominator should be coprime with 10 for a repeating
# decimal."

#     phi = totient(denominator)
#     k = 1

#     while True:
#         if pow(10, k, denominator) == 1:
#             return k
#         k += 1


def div(num, den):
    return (num // den, (num % den))


env = {}
io = remote("20.195.26.61", 1337)

io.recvline()
while True:
    next_nums = io.recvline(keepends=False)
    if b"Nope" in next_nums or b"ASCIS" in next_nums:
        io.interactive()
        break
    a, b, k = list(map(lambda x: (int(x)), next_nums.split(b" ")))
    period = totient(b)
    while a >= b:
        res, a = div(a, b)
    a *= 10
    res = 0
    print(period)
    print(k % period)
    for i in range(k % period):
        res, a = div(a, b)
        a *= 10
    print(res)
    io.sendline(str(res).encode())

    # period = totient(int(b))
    # getcontext().prec = int(period * 2)
    # print(period)
    # res = str(a / b).split(".")[-1]
    # if len(res) < period:
    #     io.sendline(b"0")
    # else:
    #     res = res[(int(k) - 1) % period]
    #     io.sendline(str(res).encode())
    # pause()
    # getcontext().prec = int(k + 1)
    # print(a / b)
    # res = str(a / b).split(".")[-1]
    # if len(res) < k:
    #     io.sendline(b"0")
    # else:
    #     # print(res)
    #     res = res[int(k) - 1]
    #     print(res)
    #     io.sendline(str(res).encode())

    # res = (a * pow(10, k) // b) % 10
    # print(res)
    # io.sendline(str(res).encode())
