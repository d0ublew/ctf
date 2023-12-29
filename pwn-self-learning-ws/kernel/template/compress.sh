#!/usr/bin/env bash

pushd ./rootfs || exit 255

find . -print0 | cpio -o --format=newc --owner=root --null >../rootfs-updated.cpio

popd || exit 255
