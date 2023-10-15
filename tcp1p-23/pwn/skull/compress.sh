#!/usr/bin/env bash

pushd ./rootfs || exit 255

find . -print0 | cpio --null -o --format=newc | gzip -9 >../initramfs-updated.cpio.gz

popd || exit 255
