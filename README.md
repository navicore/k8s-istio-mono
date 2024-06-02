
```
brew install kind
go install sigs.k8s.io/cloud-provider-kind@latest

# creates a kind cluster with name "istio-mono"
./scripts/create_kind_cluster.sh

make

# in a separate window or fork, run for load balancer
# support TODO: mac service

sudo cloud-provider-kind
```
