#!/bin/bash

FILE="/tmp/yvnyfu"

cat << EOF > /tmp/solve.py
from pwn import *

r = process('/challenge/embryoio_level20', stdout=open('${FILE}', 'w+'))
r.recvall()
r.close()
EOF

ipython <<< "run /tmp/solve.py"

cat ${FILE} | grep -oE "pwn.college{.*}"
