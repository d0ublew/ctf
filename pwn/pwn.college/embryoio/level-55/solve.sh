#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level55', stdout=PIPE)
grep = Popen(['/usr/bin/grep', '-ioE', 'pwn.college{.*}'], stdin=chall.stdout)
grep.wait(timeout=1)
EOF

python /tmp/solve.py
