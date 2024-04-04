dump: dump.s
	musl-gcc -static $< -o $@
	base64 -w0 $@ > $@.b64
	cat $@.b64 | clip

dump.s: dump.c
	gcc -S $< -o $@

test: test.c
	gcc -Wl,-z,relro $< -o $@
	patchelf --replace-needed libc.so.6 ./libc.so.6 $@
