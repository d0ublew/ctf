#!/usr/bin/env bash

./solve | nc 34.124.157.94 10541 | grep -oP "grey{.+}"
