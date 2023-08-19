#!/usr/bin/env python3

with open("./bufer.bin", "rb") as f:
    buf = f.read()


dec = bytearray()
for i in range(len(buf)):
    dec.append(buf[i] ^ 0x12)

print(dec)
