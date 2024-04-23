#!/usr/bin/env python3

from pwn import xor

key = [
    0x76, 0x22, 0x99, 0xf2, 0x11, 0x67, 0xfe, 0x66,
]

with open("./enc.txt", "rb") as f:
    enc = f.read()

dec = xor(enc, key)
print(dec)
