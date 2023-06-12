#!/usr/bin/env python3

# Ref:
# https://www.lostmyplaintext.com/project/2020/04/30/Merkle-Hellman-Knapsack-and-LLL.html

from mh import break_cipher

ct = [
    8436,
    22465,
    30044,
    22465,
    51635,
    10380,
    11879,
    50551,
    35250,
    51223,
    14931,
    25048,
    7352,
    50551,
    37606,
    39550]

pub_key = [7352, 2356, 7579, 19235, 1944, 14029, 1084]

for i in ct:
    break_cipher(i, pub_key)
