#!/usr/bin/env python3

# type: ignore

from z3 import *

passcode = [BitVec(f"p_{i}", 8) for i in range(6)]

s = Solver()
# for i in range(6):
#     s.add(passcode[i] >= ord('0'))
#     s.add(passcode[i] <= ord('9'))

s.add(passcode[0x4] == passcode[0x1] - 0x4)
s.add(passcode[0x1] == (passcode[0x0] ^ 0x44))
s.add(passcode[0x0] == passcode[0x2] - 0x7)
s.add(passcode[0x3] == (passcode[0x2] ^ 0x25))
s.add(passcode[0x5] == (passcode[0x0] ^ 0x14))
s.add(passcode[0x4] == passcode[0x1] - 0x4)
s.add(passcode[0x0] == (passcode[0x3] ^ 0x22))
s.add(passcode[0x0] == passcode[0x2] - 0x7)
s.add(passcode[0x0] == passcode[0x5] + 0xc)
s.add(passcode[0x2] == passcode[0x4] + 0x47)
s.add(passcode[0x2] == (passcode[0x5] ^ 0x13))
s.add(passcode[0x5] == (passcode[0x3] ^ 0x36))
s.add(0x52 == passcode[0x3])

if s.check() == sat:
    m = s.model()
    m_sorted = sorted([var for var in m],
                      key=lambda x: int(str(x).split("_")[-1]))
    for i in m_sorted:
        print(chr(m[i].as_long()), end='')
