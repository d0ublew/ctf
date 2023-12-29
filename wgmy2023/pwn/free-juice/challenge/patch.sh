#!/usr/bin/env bash

if [ $# -ne 1 ]; then
	echo "Missing filename" >&2
	exit 255
fi

FNAME="${1}"
cp "./${FNAME}" "./${FNAME}_patched"
patchelf --replace-needed libc.so.6 ./libc* "./${FNAME}_patched"

FOUND_INTERPRETER=$(ls | grep "^ld-.*\.so" | head)

[ -n $FOUND_INTERPRETER ] &&
	patchelf --set-interpreter ${FOUND_INTERPRETER} "./${FNAME}_patched"
