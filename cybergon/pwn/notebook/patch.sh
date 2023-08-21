#!/usr/bin/env bash

FNAME="${1}"
cp "./${FNAME}" "./${FNAME}_patched"
patchelf --replace-needed libc.so.6 ./libc.so.6 "./${FNAME}_patched"
