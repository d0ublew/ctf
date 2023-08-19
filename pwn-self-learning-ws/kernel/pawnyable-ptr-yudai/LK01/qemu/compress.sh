#!/usr/bin/env bash

pushd ./root || exit 255

find . -print0 | cpio -o --format=newc --owner=root --null > ../rootfs_updated.cpio

popd || exit 255
