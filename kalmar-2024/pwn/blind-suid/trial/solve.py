#!/usr/bin/env python3

from pwn import *

# type: ignore
# flake8: noqa


libc = ELF("./libc.so.6", checksec=False)

"""
rip: 0x7f6f3ebfd290
---
rip: 0x7f6f3e9d8dc0
---
rip: 0x7f6f3e9d8e68
---
rip: 0x7f6f3e9d8ebb
---
rip: 0x7f6f3ea0f6f0
---
rip: 0x7f6f3ea2e380
---
Password: idk
rip: 0x7f6f3eb475a0
---
rip: 0x7f6f3eb47940
---
rip: 0x7f6f3ea2fe50
---
Wrong password!
rip: 0x7f6f3e9d8d90
---
rip: 0x7f6f3e9f49a0
---
rip: 0x7f6f3ebe324e
---
rip: 0x7f6f3ebe3274
---
"""

"""
libc_base: 0x7f221d538000
rip: 0x7f221d561dc0
rip: 0x7f221d561e68
rip: 0x7f221d561ebb
rip: 0x7f221d5986f0
rip: 0x7f221d5b7380
Password: K33pth15s3Cret
rip: 0x7f221d6d05a0
rip: 0x7f221d6d0940
rip: 0x7f221d5b8e50
Correct!
rip: 0x7f221d652f20
rip: 0x7f221d561d90
rip: 0x7f221d57d9a0
rip: 0x7f221d76c24e
rip: 0x7f221d76c274
"""

addrs = [
    0x7f6f3e9d8dc0,
    0x7f6f3e9d8e68,
    0x7f6f3e9d8ebb,
    0x7f6f3ea0f6f0,
    0x7f6f3ea2e380,
    0x7f6f3eb475a0,
    0x7f6f3eb47940,
    0x7f6f3ea2fe50,
    0x7f6f3e9d8d90,
    0x7f6f3e9f49a0,
    0x7f6f3ebe324e,
    0x7f6f3ebe3274,
]

addrs = [
    0x7f221d561dc0,
    0x7f221d561e68,
    0x7f221d561ebb,
    0x7f221d5986f0,
    0x7f221d5b7380,
    # Password: K33pth15s3Cret
    0x7f221d6d05a0,
    0x7f221d6d0940,
    0x7f221d5b8e50,
    # Correct!
    0x7f221d652f20,
    0x7f221d561d90,
    0x7f221d57d9a0,
    0x7f221d76c24e,
    0x7f221d76c274,
]

libc.address = addrs[0] - libc.sym["__libc_start_main"]
log.info(f"{libc.address=:#x}")

for addr in addrs:
    libc_sym = None
    for sym, vaddr in libc.symbols.items():
        if addr == vaddr:
            libc_sym = sym
            break
    if libc_sym is not None:
        log.info(f"{addr:#x} is {libc_sym}")
    else:
        log.info(f"{addr:#x} is unknown, offset = {addr-libc.address:x}")
