all:
	gcc -z norelro -o a_no a.c
	gcc -z relro -z lazy -o a_partial a.c
	gcc -z relro -o a_full a.c
	gcc -fno-PIC -fPIE -o a_nopic_pie a.c
	gcc -fno-PIC -no-pie -o a_nopic_nopie a.c
	gcc -fno-plt -o a_noplt a.c
	gcc -fPIC -no-pie -o a_pic_nopie a.c

clean:
	rm a_*
