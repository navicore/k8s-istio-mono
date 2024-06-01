#!/bin/bash

# Check if kind cluster exists
if kind get clusters | grep -q "istio-mono"; then
  echo "Kind cluster already exists."
else
  # Create kind cluster
  kind create cluster --name istio-mono --config=kind-config.yaml
  echo "Kind cluster created."
fi

# Install Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
echo "Istio installed and sidecar injection enabled for default namespace."
