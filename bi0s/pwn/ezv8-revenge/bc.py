#!/usr/bin/env python3

import sys

with open(sys.argv[1], "rb") as f:
    bc = f.read()

arr = []
for i in bc:
    arr.append(i)

print(arr)
