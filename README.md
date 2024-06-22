Install
----------

```
brew install kind
go install sigs.k8s.io/cloud-provider-kind@latest
```

Setup
----------

Create a kind cluster with name "istio-mono"

```
make

# in a separate window or fork, run for load balancer
# support TODO: mac service

sudo cloud-provider-kind

#
# DONE
#

```
More Setup
----------

```

# monitoring

kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000:80

#    Username: admin
#    Password: prom-operator

```

Shutdown
----------

```
# TODO
```
