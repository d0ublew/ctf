#!/usr/bin/env bash

# docker rm -f chal4
# docker run --name chal4 registry.gitlab.tugraz.at/osterm/docker-challenges:chal4 /bin/true
# docker cp chal4:/app .
# docker cp chal4:/usr/local/lib/libpython3.11.so.1.0 .
# docker rm -f chal4

LD_PRELOAD=./libpython3.11.so.1.0 PYTHONHOME="${HOME}/.pyenv/versions/3.11.1" ./app
