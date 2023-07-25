#!/usr/bin/env sage

with open('./output.txt', 'r') as f:
    n, e = eval(f.readline().strip())
    coeffs = eval(f.readline().strip())


P = Zmod(n)["x"]
f = P(coeffs)
