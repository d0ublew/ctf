#!/bin/sh

# /usr/bin/qemu-system-x86_64 \
# 	-m 128M \
# 	-cpu kvm64,+smep,+smap \
# 	-nographic \
# 	-monitor /dev/null \
# 	-kernel bzImage \
# 	-initrd initramfs.cpio.gz \
# 	-no-reboot \
# 	-append "console=ttyS0 quiet kaslr panic=1 kpti=1 oops=panic"

/usr/bin/qemu-system-x86_64 \
	-m 128M \
	-cpu kvm64,+smep,+smap \
	-nographic \
	-monitor /dev/null \
	-kernel bzImage \
	-initrd initramfs-updated.cpio.gz \
	-no-reboot \
	-append "console=ttyS0 quiet kaslr panic=1 kpti=1 oops=panic"
