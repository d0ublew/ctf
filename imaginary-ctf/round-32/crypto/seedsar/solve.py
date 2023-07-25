#!/usr/bin/env python3

from random import randint, seed
from tqdm import trange

ct = b']lFKQGuMKHkt7\'WnRM^H~|<)QmO=7Yo*1}5/q](1hH&y RG$v|RI5&=>>SBg{=Ea5q,V,b_Q\'cM%cBs-G9^nn*i~;%pWBe?,bQKe]g%]9\\L_x!"V::MG2hR,/yr<K}wA}JKH&<O/^#igA@|{*`oB"a<~'
alphabet = bytes(range(32, 127))
LIMIT = 10**8

known = b'ictf{'

"""
'i' + key == ']' mod len(alphabet)
key == ']' - 'i' mod len(alphabet)
"""

key = (alphabet.index(b']') - known[0]) % len(alphabet)


def f(x, y):
    return (alphabet.index(x) - y) % len(alphabet)


keys = []
for i in trange(key, LIMIT + 1, len(alphabet)):
    if f(ct[0], i) == known[0] % len(alphabet):
        seed(i)
        tmp_key = randint(0, LIMIT)
        if f(ct[1], tmp_key) == known[1] % len(alphabet):
            seed(tmp_key)
            tmp_key = randint(0, LIMIT)
            if f(ct[2], tmp_key) == known[2] % len(alphabet):
                seed(tmp_key)
                tmp_key = randint(0, LIMIT)
                if f(ct[3], tmp_key) == known[3] % len(alphabet):
                    seed(tmp_key)
                    tmp_key = randint(0, LIMIT)
                    if f(ct[4], tmp_key) == known[4] % len(alphabet):
                        keys.append(i)


def seedsar(s, key):
    out = []
    for c in s:
        o = (alphabet.index(c) - key) % len(alphabet)
        if o < 32:
            o += 95
        elif o > 127:
            o -= 95
        out.append(o)
        seed(key)
        key = randint(0, LIMIT)
    return bytes(out)


for key in keys:
    print(seedsar(ct, key))
