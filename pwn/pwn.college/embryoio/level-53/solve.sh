#!/bin/bash

cat << EOF > /tmp/solve.py
from subprocess import Popen, PIPE

rev = Popen('/usr/bin/rev', stdin=PIPE, stdout=PIPE)
rev.stdin.write(b"iaydzola"[::-1])

chall = Popen('/challenge/embryoio_level53', stdin=rev.stdout)
chall.wait(timeout=1)
EOF

ipython <<< "run /tmp/solve.py"
