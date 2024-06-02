
```
brew install kind
go install sigs.k8s.io/cloud-provider-kind@latest

./scripts/create_kind_cluster.sh

make

#run for load balancer support TODO: mac service
sudo cloud-provider-kind logs --name istio-mono

```
