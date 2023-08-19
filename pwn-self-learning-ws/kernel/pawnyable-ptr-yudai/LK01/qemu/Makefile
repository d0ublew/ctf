all:
	gcc -S -o exploit.s exploit.c
	musl-gcc -static -o exploit exploit.s
	cp exploit ./root/exploit
	./compress.sh
	./run.sh
