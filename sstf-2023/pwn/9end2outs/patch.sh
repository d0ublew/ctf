#!/usr/bin/env bash

cp ./9end2outs ./9end2outs_patched
patchelf --replace-needed libc.so.6 ./libc.so.6 ./9end2outs_patched
