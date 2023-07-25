#!/usr/bin/env python3

import binascii
import itertools
import sys

with open("./asd.txt", "r") as f:
    enc = f.read()


hx = list("0123456789abcdef")
em = list("~!@#$%^&*()-=_+?")

pattern = "696374667b"

substr = []

for i in range(len(enc)):
    if i + 10 > len(enc):
        break
    substr.append(enc[i:i + 10])

match = ""
idx = 0
for s in substr:
    if s[0] != s[2]:
        continue
    if s[0] != s[6]:
        continue
    if s[0] != s[7]:
        continue
    if s[0] != s[2]:
        continue
    if s[4] != s[8]:
        continue
    match = s
    idx = substr.index(s)
    break

submatch = set(zip(list(match), list(pattern)))

for e, c in submatch:
    enc = enc.replace(e, c)

enc = enc.replace("*", "0")
enc = enc.replace("!", "d")
enc = enc.replace(")", "f")
enc = enc.replace("_", "5")
enc = enc.replace("+", "2")
enc = enc.replace("#", "c")
enc = enc.replace("?", "e")
enc = enc.replace("=", "1")
enc = enc.replace("$", "8")
enc = enc.replace("^", "a")

stats = {}

for i in range(0, len(enc), 2):
    try:
        print(binascii.unhexlify(enc[i:i + 2]).decode(), end='')
    except BaseException:
        if enc[i:i + 2] not in stats:
            stats[enc[i:i + 2]] = 0
        else:
            stats[enc[i:i + 2]] += 1
        print(f"[{enc[i:i + 2]}]", end='')

print()
print(sorted(stats, key=lambda x: x[1], reverse=False))
