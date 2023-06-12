#!/usr/bin/env sage


with open("./Check_number_63/output.txt") as f:
    n = int(f.readline().strip().split(" = ")[-1])
    es = f.readlines()

var('d,p,q')

eqs = []

for e in es:
    e, r = list(map(int, e.strip().split(":")))
    eqs.append((d*e - 1) == r * (p-1) * (q-1))
