#!/usr/bin/env bash

for i in $(seq 0 2023 | tac); do
	tar xvf "./UniKL${i}.tar"
done
