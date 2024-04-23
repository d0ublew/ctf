#!/usr/bin/env python3

with open("./output.txt", "r") as f:
    enc = f.read().split("\n")


known = b"TCP1"

key_1 = len(enc[0]) // known[0]
key_2 = len(enc[1]) // known[1]

assert (len(enc[2]) // known[2] == key_1)
assert (len(enc[3]) // known[3] == key_2)

flag = ""
for i in range(len(enc)):
    if i % 2 == 0:
        flag += chr(len(enc[i]) // key_1)
    else:
        flag += chr(len(enc[i]) // key_2)

print(flag)
