#!/usr/bin/env python3

# type: ignore

import ctypes
import sys

from capstone import *
from capstone.x86 import *

with open("./sc1.bin", "rb") as f:
    sc = f.read()


md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

asm = {}

# sc_call = None
for (address, *i) in md.disasm_lite(sc, len(sc)):
    # if i[1] == "call" and "0x" not in i[2]:
    #     sc_call = address
    asm[address] = i

vtable = {
}

base = list(asm.keys())[0]
print(hex(base))
# print(hex(sc_call - base))
# quit()

pie = 0xa90000


def rebase(addr):
    return addr - base + pie


try:
    eip = int(sys.argv[1], 16)
    if sys.argv[2] is not None:
        eip = eip - pie + base
        print(hex(eip), hex(max(asm.keys())))
except IndexError:
    eip = base

counter = 0
cache = []
last = None
last_reg = None
while eip <= max(asm.keys()):
    if counter > 1000:
        quit()
    inst = asm[eip]
    if inst[1] == "jmp" and "0x" in inst[2]:
        eip = int(inst[2], 16)
        continue
    counter += 1
    if inst[1] == "call":
        last = None
        last_reg = None
        cache = []
        if "dword ptr [0x4" in inst[2]:
            k = inst[2].split("[")[-1][:-1]
            print(hex(rebase(eip)), inst[1], vtable[int(k, 16)])
        else:
            print(hex(rebase(eip)), ' '.join(inst[1:]))
    elif inst[1] == "mov" and "ptr" not in inst[2] and "0x" in inst[2] and "ebp" not in inst[2] and "esp" not in inst[2]:
        last_reg = inst[2].split(', ')[0]
        cache.append((eip, inst))
    elif len(cache) > 0 and inst[1] in ["xor", "sub", "add"] and "ptr" not in inst[2] and inst[2].split(', ')[0] == last_reg and "0x" in inst[2]:
        cache.append((eip, inst))
    else:
        if len(cache) > 0:
            op_str = cache.pop(0)[-1][-1].split(', ')
            reg = op_str[0]
            imm = int(op_str[1], 16)
            acc = imm
            for pc, i in cache:
                _op_str = i[-1].split(', ')
                _imm = int(_op_str[1], 16)
                if i[1] == "add":
                    acc += _imm
                elif i[1] == "sub":
                    acc -= _imm
                elif i[1] == "xor":
                    acc ^= _imm
                else:
                    raise NotImplementedError(i[1])
                acc = ctypes.c_uint32(acc).value
            print(f"{reg} = {acc:#x} ({ctypes.c_int32(acc).value:#x})")
            cache = []
            last_reg = None
        print(hex(rebase(eip)), ' '.join(inst[1:]))
    if inst[1] == "ret":
        quit()
    last = inst[1:]
    eip += inst[0]
