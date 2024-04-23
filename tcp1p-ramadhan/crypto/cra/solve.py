#!/usr/bin/env python3

# type: ignore

import gmpy2
from Crypto.Util.number import long_to_bytes

with open("./output.txt", "r") as f:
    enc = int(f.read().strip())

flag, _ = gmpy2.iroot(enc, 3)

print(long_to_bytes(flag))
