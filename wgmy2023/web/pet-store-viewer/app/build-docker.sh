#!/bin/sh

docker build . -t wgmy2023-storeviewer
docker run --rm --name=wgmy2023-storeviewer -p 8222:5000 wgmy2023-storeviewer