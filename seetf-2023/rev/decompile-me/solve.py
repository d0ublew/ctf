#!/usr/bin/env python3

from pwn import xor

with open('output.txt', 'rb') as f:
    enc = f.read()

a = enc[:9]  # orig_b ^ orig_c
b = enc[9:18]  # orig_a ^ orig_c ^ 9
c = enc[18:]  # orig_b ^ 14

x = int(str(len(enc))[0]) + int(str(len(enc))[1])
y = int(str(len(enc))[0]) * int(str(len(enc))[1])

orig_b = xor(c, y)
orig_c = xor(xor(a, c), y)
orig_a = xor(xor(b, orig_c), x)

print(orig_a + orig_b + orig_c)
