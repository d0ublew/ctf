#!/bin/bash

TEMP=$(mktemp)

echo -ne "LETMEWIN\n" > ${TEMP}

./fd 4660 < ${TEMP}

rm ${TEMP}
