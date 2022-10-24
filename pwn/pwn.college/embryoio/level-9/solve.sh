#!/bin/bash

cat << EOF > /tmp/shell.sh
#!/bin/bash

/challenge/embryoio_level9
EOF

bash /tmp/shell.sh <<< "pfcooanp"
