#!/usr/bin/env python3

# type: ignore

from typing import List

from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

with open('./sc1337.bin', 'rb') as f:
    sc = f.read()


for inst in md.disasm(sc, len(sc)):
    print(inst.address, inst.mnemonic, inst.op_str)
