#!/usr/bin/env bash

socat tcp-l:1337,fork exec:"qemu-aarch64-static -g 1234  -L /usr/aarch64-linux-gnu ./vuln",reuseaddr
