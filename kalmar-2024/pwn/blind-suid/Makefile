BIN=dump
.PHONY: $(BIN).c test

$(BIN): $(BIN).c
	musl-gcc -static $< -o $@
	base64 -w0 $@ > $@.b64
	cat $@.b64 | clip.exe

# $(BIN).s: $(BIN).c
# 	gcc -S $< -o $@

test: mysudo.c
	gcc -w -pie -Wl,-z,relro mysudo.c -o mysudo
	patchelf --replace-needed libc.so.6 ./libc-2.35.so.6 mysudo
	patchelf --set-interpreter ./ld-2.35.so mysudo
	# sudo chown root:root mysudo
	# sudo chmod 4711 mysudo
