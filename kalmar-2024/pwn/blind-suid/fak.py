#!/usr/bin/env python3

# type: ignore

import string

from z3 import *


def rol(x, n):
    return (shl(x, n) | (shr(x, 64 - n)))


def shr(x, n):
    return (x >> n) & (2**(64 - n) - 1)


def shl(x, n):
    return (x << n) & (2**64 - 1)


def main():
    s = Solver()

    k = 4
    args = [BitVec(f"arg_{i}", 64) for i in range(k)]
    for i in range(len(args)):
        s.add(args[i] >= 0)
        s.add(args[i] <= 25)

    # s.add(args[0] == string.ascii_lowercase.index('h'))
    # s.add(args[2] == string.ascii_lowercase.index('l'))

    v7 = BitVecVal(1, 64)
    for i in args:
        v7 = v7 * 26 + i

    # v7 = simplify(v7)

    v8 = rol(v7 ^ 0xAAAAAAAAAAAAAAAA, 20)
    for _ in range(16):
        v9 = shl(shr(v8, 12) ^ v8, 25) ^ shr(v8, 12) ^ v8
        v8 = shr(v9, 27) ^ v9
    s.add(v8 == 0x39403F5DA078C2A)   # win
    # s.add(v8 == 0xEFCD7BDD75FB0253)  # sleep 5 => zzz
    # s.add(v8 == 0x49AE4D04A4B5EA08)  # id => id
    # s.add(v8 == 0xA6E3B88D6AF92999)  # head => flag
    # s.add(v8 == 0x39EDA4A27C0507AB)  # puts('Run command as root') => help

    if s.check() == sat:
        m = s.model()
        m_sorted = sorted([var for var in m],
                          key=lambda x: int(str(x).split("_")[-1]))
        for i in m_sorted:
            print(string.ascii_lowercase[m[i].as_long()], end='')
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
