#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level59', stdin=PIPE)
rev = Popen(['/usr/bin/rev'], stdin=PIPE, stdout=chall.stdin)
rev.stdin.write(b'bykdizxw'[::-1])
chall.wait(timeout=1)

EOF

python /tmp/solve.py
