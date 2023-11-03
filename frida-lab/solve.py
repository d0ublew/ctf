#!/usr/bin/env python3

# type: ignore

import logging
import sys

import frida

process_name = "FridaLab"
device = frida.get_usb_device()

target_process = device.get_process(process_name)
session = device.attach(target_process.pid)
print(f"[*] Attached to {process_name} (pid: {target_process.pid})")

chall06_counter = 0
chall06_solved = False


def message_handler(message, data):
    global chall06_counter
    global chall06_solved
    if message["type"] == "error":
        print(message)
        return
    payload = message["payload"]
    if message["type"] == "send":
        if "addChall06" in payload:
            chall06_counter += 1
        elif "invoked MainActivity.chall06" in payload:
            chall06_solved = True
        else:
            print(f"[*] {payload}")
    if data is not None and "addChall06" not in payload:
        print(f"[*] data: {data}")
    if chall06_counter > 10 and data is not None and not chall06_solved:
        print("[*] chall06 is solvable now!")
        script.post({"type": "chall06_solver", "arg": data[0]})


with open("./solve.js") as f:
    jscode = f.read()
script = session.create_script(jscode)
script.on("message", message_handler)
script.load()
try:
    sys.stdin.read()
except BaseException:
    session.detach()
    print("\n[*] Detached successfully")
