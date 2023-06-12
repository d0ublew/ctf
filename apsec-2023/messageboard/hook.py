#!/usr/bin/env python3

import frida
import sys
import time


def message_handler(message, payload):
    print()
    print(f"[!] message: {message}")
    print(f"[!] payload: {payload}")


with open(sys.argv[1]) as f:
    jscode = f.read()

# Get IP from Genymotion settings button on bottom right corner
device = frida.get_device_manager().add_remote_device("192.168.123.105")

session = None

if sys.argv[2] == "attach":
    # Need to invoke `frida-ps` before using the matching process name
    print("[*] Attaching to existing process")
    session = device.attach(sys.argv[3])
    pid = repr(session)[12:-1]
    print(f"[*] Attached to process (pid={pid})")

elif sys.argv[2] == "spawn":
    print(f"[*] Spawning {sys.argv[3]} application")
    pid = device.spawn([sys.argv[3]])
    print(f"[*] Application spawned successfully (pid={pid})")
    print(f"[*] Attaching to spawned process (pid={pid})")
    session = device.attach(pid)
    print(f"[*] Attached to process (pid={pid})")
    device.resume(pid)
    time.sleep(2)

script = session.create_script(jscode)
script.on("message", message_handler)
script.load()
try:
    sys.stdin.read()
except KeyboardInterrupt:
    print(f"\n[*] Detaching from process (pid={pid})")
    session.detach()
    print(f"[*] Successfully detached from process (pid={pid})")
    if sys.argv[2] == "spawn":
        print(f"[*] Killing process (pid={pid})")
        device.kill(pid)
        print(f"[*] Killed process (pid={pid})")
