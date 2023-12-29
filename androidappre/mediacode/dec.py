#!/usr/bin/env python3

a = bytearray()

for i in range(26):
    a.append(i + 65)

for i in range(26):
    a.append(i + 97)

for i in range(10):
    a.append(i + 48)

a_ = bytes(a) + b"-./:_ =,?"


def dec(e):
    result = bytearray()
    for i in e:
        result.append(a_[i])
    return bytes(result)


e = [18, 33, 30, 37, 37, 17, 30, 28, 30, 34, 47, 30, 43]
e = [26, 28, 45, 34, 40, 39, 53, 32, 30, 45, 26, 41, 41, 56, 44, 45, 26, 43,
     45]
e = [57, 3, 57, 0, 4, 4, 60, 61, 65, 3, 58, 57, 57, 66, 3, 3,
     63, 58, 3, 1, 63, 1, 58, 63, 1, 0, 4, 64, 60, 64, 1, 0]

print(dec(e))
