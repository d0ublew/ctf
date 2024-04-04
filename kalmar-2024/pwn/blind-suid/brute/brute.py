#!/usr/bin/env python3

import itertools
import string

import tqdm


def rol(x, n):
    return (shl(x, n) | (shr(x, 64 - n)))


def shr(x, n):
    return (x >> n) & (2**(64 - n) - 1)


def shl(x, n):
    return (x << n) & (2**64 - 1)


def myhash(x):
    v7 = 1
    for i in x:
        v7 *= 26
        v7 += i
    v8 = rol(v7 ^ 0xAAAAAAAAAAAAAAAA, 20)
    for _ in range(16):
        v9 = shl(shr(v8, 12) ^ v8, 25) ^ shr(v8, 12) ^ v8
        v8 = shr(v9, 27) ^ v9
    if v8 >= 2**64:
        raise OverflowError("Int Overflow")
    return v8


a = itertools.product(range(26), repeat=7)

commands = [
    0x39403F5DA078C2A,
    0xEFCD7BDD75FB0253,
    0x49AE4D04A4B5EA08,
    0xA6E3B88D6AF92999,
    0x39EDA4A27C0507AB,
]

result = None
for c in tqdm.tqdm(a):
    out = myhash(c)
    if out == 0x39403F5DA078C2A:
        result = ''.join(map(lambda x: string.ascii_lowercase[x], c))
        break

print()
print(result)
