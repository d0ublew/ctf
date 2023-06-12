#!/usr/bin/env python3

from binascii import unhexlify

with open("spi.txt", "r") as f:
    logs = f.readlines()


command = {
    0: {
        "arg": False,
        "desc": "Tell the card to reset and enter its idle state",
    },
    16: {
        "arg": True,
        "desc": "Select the block length",
    },
    17: {
        "arg": True,
        "desc": "Read a single block",
    },
    24: {
        "arg": True,
        "desc": "Write a single block",
    },
    55: {
        "arg": False,
        "desc": "Next command will be application specific (ACMDXX)",
    },
    58: {
        "arg": False,
        "desc": "Read OCR"
    }
}

read_block = {}

read = False

for log in logs:
    traffic, data = log.strip().split(" : ")
    if read and traffic == "SD Card to Device":
        if len(data) == 2:
            continue
        read_block[arg] = unhexlify(data)

    if traffic == "Device to SD Card":
        read = False
        data = int(data, 16)
        cmd = (data & 0x3f0000000000) >> 40
        arg = (data & 0x00ffffffff00) >> 8
        if cmd != 17:
            continue
        read = True
        try:
            print(command[cmd]["desc"])
            if command[cmd]["arg"]:
                print(f"Argument: {hex(arg)}")
            print()
        except KeyError:
            print("command not found")

with open('dump', 'wb') as f:
    for key in sorted(read_block):
        if key > 61:
            continue
        a = bytearray(read_block[key]).index(b"\xfe")
        data = read_block[key][a + 1:-2]  # last 2 byte is CRC
        f.write(data)
