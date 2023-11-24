#!/bin/bash

cp ./chal ./chal_patched
patchelf --set-interpreter ./ld-linux-x86_64.so.2 ./chal_patched
