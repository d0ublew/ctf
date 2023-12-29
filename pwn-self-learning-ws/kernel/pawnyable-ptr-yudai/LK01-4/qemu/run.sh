#!/bin/sh
qemu-system-x86_64 \
	-s \
	-m 64M \
	-nographic \
	-kernel bzImage \
	-append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
	-no-reboot \
	-cpu qemu64,+smap,+smep \
	-smp 4 \
	-monitor telnet::45454,server,nowait \
	-serial mon:stdio \
	-initrd rootfs-updated.cpio \
	-net nic,model=virtio \
	-net user
