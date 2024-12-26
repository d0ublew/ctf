#!/usr/bin/env bash

set -xe

podman --remote kube down ./rigged2-deployment.yaml

pushd ./challenge/ && podman --remote build -t rigged2 . && popd

podman --remote kube play ./rigged2-deployment.yaml
