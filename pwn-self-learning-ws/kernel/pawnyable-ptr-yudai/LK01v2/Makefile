CC=gcc
CFLAGS=-S

all:
	$(CC) $(CFLAGS) -o pwn.s pwn.c
	musl-gcc -static -o pwn pwn.s
	# cp pwn ./rootfs/pwn
	# ./compress.sh
	# ./run.sh

debug:
	$(CC) $(CFLAGS) -DDEBUG -o pwn.s pwn.c
	musl-gcc -static -o pwn pwn.s

