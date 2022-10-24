#!/bin/bash

cat << EOF > /tmp/shell.sh
#!/bin/bash

env -i /challenge/embryoio_level14
EOF

bash /tmp/shell.sh
