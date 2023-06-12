#!/usr/bin/env bash


docker rmi -f gotcha
docker build -t gotcha .
