#!/bin/bash

cat << EOF > /tmp/shell.sh
#!/bin/bash

/challenge/embryoio_level13 > /tmp/ctvuqc
EOF

bash /tmp/shell.sh
cat /tmp/ctvuqc
