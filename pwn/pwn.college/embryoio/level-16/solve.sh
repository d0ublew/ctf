#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
r = process(['/challenge/embryoio_level16'])
r.sendlineafter(b'your input now...\n', b"tymtxmra")
print(r.recvall().decode())
EOF

ipython <<< "run /tmp/solve.py" | grep -oE "pwn.college{.*}"
