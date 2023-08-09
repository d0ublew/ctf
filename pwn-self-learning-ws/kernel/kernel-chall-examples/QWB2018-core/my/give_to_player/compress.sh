#!/usr/bin/env bash

gcc -static -o ./fs/solve solve.c || exit 255
pushd ./fs

find . -print0 | \
    cpio --null -ov --format=newc | \
    gzip -9 > ../core.cpio

popd
