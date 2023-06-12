#!/usr/bin/env sage

n = 10 ^ 128
print(solve_mod(x == pow(x, 10), n))
