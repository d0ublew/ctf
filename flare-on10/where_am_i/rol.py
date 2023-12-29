#!/usr/bin/env python3

import sys


def rol(x, n):
    return ((x << n) | (x >> (0x20 - n))) & 0xffffffff


x = int(sys.argv[1], 16)
n = int(sys.argv[2], 16)

print(hex(rol(x, n)))
