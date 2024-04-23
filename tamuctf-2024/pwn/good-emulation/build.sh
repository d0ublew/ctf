#!/usr/bin/env bash

podman build --build-arg-file ./argfile.conf -t good-emu .
