#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
r = process(['/challenge/embryoio_level15'])
print(r.recvall().decode())
EOF

ipython <<< "run /tmp/solve.py" | grep -oE "pwn.college{.*}"
