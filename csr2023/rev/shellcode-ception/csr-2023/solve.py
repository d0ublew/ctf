#!/usr/bin/env python3

from capstone import *
from pwn import p16, p32, p64, xor

with open("./enc.sc", "rb") as f:
    sc = f.read()

sc = xor(sc, 0x69)

with open("./dec.sc", "wb") as f:
    f.write(sc)

# md = Cs(CS_ARCH_X86, CS_MODE_64)
#
# for i in md.disasm(sc[:0x98], 0):
#     print(f"{i.address:#x}: {i.mnemonic} {i.op_str}")

"""
0x0: push rbp
0x1: mov rbp, rsp
0x4: movabs rax, 0x2a2275313a131202
0xe: movabs rdx, 0x72222f701e262f28
0x18: mov qword ptr [rbp - 0x30], rax
0x1c: mov qword ptr [rbp - 0x28], rdx
0x20: movabs rax, 0x75221e2f71703531
0x2a: movabs rdx, 0x2f2f751e24231e2f
0x34: mov qword ptr [rbp - 0x20], rax
0x38: mov qword ptr [rbp - 0x18], rdx
0x3c: mov dword ptr [rbp - 0x10], 0x2f70382e
0x43: mov word ptr [rbp - 0xc], 0x3c26
0x49: mov byte ptr [rbp - 0xa], 0
0x4d: mov dword ptr [rbp - 4], 0
0x54: jmp 0x72
0x56: mov eax, dword ptr [rbp - 4]
0x59: cdqe
0x5b: movzx eax, byte ptr [rbp + rax - 0x30]
0x60: xor eax, 0x41
0x63: mov edx, eax
0x65: mov eax, dword ptr [rbp - 4]
0x68: cdqe
0x6a: mov byte ptr [rbp + rax - 0x30], dl
0x6e: add dword ptr [rbp - 4], 1
0x72: cmp dword ptr [rbp - 4], 0x25
0x76: jle 0x56
0x78: mov dword ptr [rbp - 8], 0
0x7f: jmp 0x8f
0x81: mov eax, dword ptr [rbp - 8]
0x84: cdqe
0x86: mov byte ptr [rbp + rax - 0x30], 0
0x8b: add dword ptr [rbp - 8], 1
0x8f: cmp dword ptr [rbp - 8], 0x25
0x93: jle 0x81
0x95: nop
0x96: pop rbp
0x97: ret
"""

enc = p64(0x2a2275313a131202)
enc += p64(0x72222f701e262f28)
enc += p64(0x75221e2f71703531)
enc += p64(0x2f2f751e24231e2f)
enc += p32(0x2f70382e)
enc += p16(0x3c26)

print(xor(enc, 0x41))
