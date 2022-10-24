#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
r = process('/challenge/embryoio_level23')
r.sendlineafter(b"input now...\n", b"lkghreha")
print(r.recvall().decode())
EOF

python /tmp/solve.py | grep -oE "pwn.college{.*}"
