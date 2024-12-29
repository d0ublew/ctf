#!/bin/bash

set -euo pipefail

#####

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#####

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.31.1+k3s1 sh -

#####

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

#####

sudo docker build -t dart:0.1.0 ./src/dart/
sudo docker save -o /tmp/dart.tar dart:0.1.0
sudo k3s ctr images import /tmp/dart.tar
sudo rm /tmp/dart.tar

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

sudo -E kubectl apply -f - <<EOF
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: ratelimit
spec:
  rateLimit:
    average: 10
    burst: 10
EOF

sudo -E helm repo add hashicorp https://helm.releases.hashicorp.com
sudo -E helm upgrade -i -n vault --create-namespace -f ./charts/vault.values.yaml vault hashicorp/vault --version 0.28.1
sudo -E helm upgrade -i -n dart --create-namespace -f ./charts/dart.values.yaml dart ./charts/dart
sudo -E helm upgrade -i -n nginx --create-namespace -f ./charts/nginx.values.yaml nginx ./charts/nginx
