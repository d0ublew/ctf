#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level58', stdin=PIPE)
cat = Popen(['/usr/bin/cat'], stdin=PIPE, stdout=chall.stdin)
cat.stdin.write(b'gptqqubu')
chall.wait(timeout=1)

EOF

python /tmp/solve.py
