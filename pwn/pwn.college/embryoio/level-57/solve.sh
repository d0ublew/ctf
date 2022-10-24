#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

chall = Popen('/challenge/embryoio_level57', stdout=PIPE)
rev1 = Popen('/usr/bin/rev', stdin=chall.stdout, stdout=PIPE)
rev2 = Popen('/usr/bin/rev', stdin=rev1.stdout)
rev2.wait(timeout=1)
EOF

python /tmp/solve.py
