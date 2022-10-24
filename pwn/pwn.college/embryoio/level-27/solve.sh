#!/bin/bash

FILE="/tmp/abccgt"

cat << EOF > /tmp/solve.py
from pwn import *

r = process('/challenge/embryoio_level27', stdout=open('${FILE}', 'w'))
r.interactive()
r.close()
EOF

python /tmp/solve.py

cat ${FILE} | grep -oE "pwn.college{.*}"
