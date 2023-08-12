#!/usr/bin/env bash

ropr -u --range '0xffffffff81000000-0xffffffff81e0b000' \
    -R "${1}" \
    ./vmlinux
