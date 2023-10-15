all:
	gcc -S -o exploit.s exploit.c
	musl-gcc -static -o exploit exploit.s
	cp exploit ./rootfs/exploit
	cp exploit ./rootfs/root/exploit
	cp exploit ./rootfs/home/blud/exploit
	./compress.sh
	tar czf ./exploit.tar.gz ./exploit
	./run.sh
