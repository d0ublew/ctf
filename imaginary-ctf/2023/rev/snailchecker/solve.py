#!/usr/bin/env python3

# type: ignore

import itertools
import math

from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b


def enc(n):
    if n == 0:
        return 0
    nearest_2_n = int(2 ** (math.log2(n) // 1))
    return 2 * (n - nearest_2_n + 1) - 1


def dec(n):
    smallest = (n - 1) // 2 + int(2**(math.log2(n) // 1))
    smallest += 1
    distance = int(2**(math.log2(n) // 1))
    res = []
    while smallest < 2**32:
        if l2b(smallest).isascii():
            res.append(l2b(smallest)[::-1].decode())
        smallest += distance
        distance *= 2

    return res


out = b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde'


flag = b""

comb = []
for n in [out[i:i + 4] for i in range(0, len(out), 4)]:
    n = b2l(n)
    comb.append(dec(n))

for f in list(itertools.product(*comb)):
    print(''.join(list(map(str, f))))
