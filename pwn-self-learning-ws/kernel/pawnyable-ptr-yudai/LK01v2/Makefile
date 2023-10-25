all:
	gcc -S -o pwn.s pwn.c
	musl-gcc -static -o pwn pwn.s
	# cp pwn ./rootfs/pwn
	# ./compress.sh
	# ./run.sh
