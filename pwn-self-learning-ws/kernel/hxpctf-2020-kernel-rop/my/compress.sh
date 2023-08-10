#!/usr/bin/env bash

gcc -static -o ./initramfs/solve solve.c || exit 255
pushd ./initramfs || exit 255
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
popd || exit 255
