#!/bin/bash

cat << EOF > /tmp/solve.py
from pwn import *
r = process(['/challenge/embryoio_level24', 'qmokszbpbn'])
print(r.recvall().decode())
EOF

python /tmp/solve.py | grep -oE "pwn.college{.*}"
