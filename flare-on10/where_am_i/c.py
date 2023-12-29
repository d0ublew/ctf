#!/usr/bin/env python3

import ctypes

a = 0xb7e15163
for i in range(0x23):
    a += 0x9e3779b9
    a = ctypes.c_uint32(a).value
    print(hex(a))
