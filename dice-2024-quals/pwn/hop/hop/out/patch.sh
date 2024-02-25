#!/usr/bin/env bash

cp ./js ./js_patched
patchelf --replace-needed libc.so.6 ./libc.so.6 js_patched
patchelf --replace-needed libstdc++.so.6 ./libstdc++.so.6.0.30 js_patched
patchelf --replace-needed libm.so.6 ./libm.so.6 js_patched
patchelf --replace-needed libcrypt.so.1 ./libcrypt.so.1.1.0 js_patched
patchelf --replace-needed libgcc_s.so.1 ./libgcc_s.so.1 js_patched
patchelf --replace-needed libcrypt.so.1 ./libcrypt.so.1 js_patched
patchelf --set-interpreter ./ld-linux-x86-64.so.2 ./js_patched
# patchelf --set-rpath . js_patched
