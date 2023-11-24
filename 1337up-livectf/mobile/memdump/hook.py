#!/usr/bin/env python3

# type: ignore

import logging
import sys

import frida

process_name = "com.example.mynative"
device = frida.get_usb_device()

target_process = device.get_process(process_name)
session = device.attach(target_process.pid)
print(f"[*] Attached to {process_name} (pid: {target_process.pid})")


def message_handler(message, data):
    if message["type"] == "error":
        print(message)
        return
    payload = message["payload"]
    if message["type"] == "send":
        print(f"[*] {payload}")


with open("./hook.js") as f:
    jscode = f.read()
script = session.create_script(jscode)
script.on("message", message_handler)
script.load()
try:
    sys.stdin.read()
except BaseException:
    session.detach()
    print("\n[*] Detached successfully")
