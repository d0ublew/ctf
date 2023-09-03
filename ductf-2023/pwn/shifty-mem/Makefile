all:
		gcc -S -o solve.s solve.c
		musl-gcc -static -o solve solve.s
		gcc -S -o race.s race.c
		musl-gcc -static -o race race.s
		rm solve.tar.gz
		tar czf solve.tar.gz solve race
