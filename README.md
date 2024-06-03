
```
brew install kind
go install sigs.k8s.io/cloud-provider-kind@latest

# creates a kind cluster with name "istio-mono"
./scripts/create_kind_cluster.sh

make

# in a separate window or fork, run for load balancer
# support TODO: mac service

sudo cloud-provider-kind

# monitoring

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000:80

#    Username: admin
#    Password: prom-operator

```
