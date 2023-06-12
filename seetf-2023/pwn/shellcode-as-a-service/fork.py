#!/usr/bin/env python3

# type: ignore
# flake8: noqa

import sys
import asyncio
from asyncio.subprocess import PIPE, STDOUT

# flag = sys.argv[1]
# alpha = sys.argv[2]
flag = "SEE{n1c3_sh3llc0ding_d6e25f87c7ebeef6e80df23d32c42d00}"
alpha = "}0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" or sys.argv[2]


async def solve(args, timeout=None):
    global wrong
    process = await asyncio.create_subprocess_exec(*args,
                                                   stdout=PIPE,
                                                   stderr=STDOUT)
    while True:
        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout)
            # sys.stdout.write(line.decode("utf-8"))
        except asyncio.TimeoutError:
            pass
        else:
            if not line:
                break
            elif b"Got EOF" in line:
                wrong = True
                process.kill()
            else:
                continue
        process.kill()
        break
    return await process.wait()

loop = asyncio.get_event_loop()
while flag[-1] != "}":
    for c in alpha:
        print(f"Trying: {c}")
        wrong = False
        args = [
            "/usr/bin/env",
            "python3",
            "./solve.py",
            f"{len(flag)}",
            f"{ord(c)}",
            "REMOTE",
            "HOST=win.the.seetf.sg",
            "PORT=2002",
        ]
        rc = loop.run_until_complete(solve(args, timeout=5))
        if not wrong:
            flag += c
            print(f"{flag=}")
            break
loop.close()
