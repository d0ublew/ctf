#!/usr/bin/env python3


data = [
    121,
    66,
    71,
    65,
    229,
    176,
    150,
    150,
    43,
    107,
    209,
    212,
    12,
    217,
    16,
    222,
    129,
    189,
    55,
    185,
    82,
    127,
    229,
    47,
    45,
    178,
    252,
    11,
    107,
    43,
    31,
    114,
    20,
    97,
    229,
    185,
    237,
    55,
    252,
    87,
    12,
    168,
    75,
    222,
    121,
    5]

key = [31, 41, 59, 265]

flag = bytearray()
for i in range(len(data)):
    for val in range(256):
        if (key[i % 4] * val & 255) == data[i]:
            flag.append(val)
            break

print(flag)
