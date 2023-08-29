#!/bin/bash

#
# build root fs
#
pushd ./fs || exit 255
find . -print0 | cpio --null -ov --format=newc | \
    gzip -9 > ../initramfs-updated.cpio.gz
popd || exit 255

#
# launch
#
/usr/bin/qemu-system-x86_64 \
	-kernel ./bzImage \
	-initrd ./initramfs-updated.cpio.gz \
	-fsdev local,security_model=passthrough,id=fsdev0,path=./workspace \
	-device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=hostshare \
	-nographic \
    -no-reboot \
	-monitor none \
	-s \
	-append "console=ttyS0 nokaslr quiet panic=1"
