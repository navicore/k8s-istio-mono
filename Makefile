.PHONY: all build deploy

all: build deploy

build:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	cd services/consume && docker build -t consume-service:latest .
	cd services/restock && docker build -t restock-service:latest .
	cd services/inventory && docker build -t inventory-service:latest .
	kind load docker-image consume-service:latest --name istio-mono
	kind load docker-image restock-service:latest --name istio-mono
	kind load docker-image inventory-service:latest --name istio-mono


deploy:
	kubectl apply -f k8s/gateway.yaml
	kubectl apply -f k8s/inventory-service.yaml
	kubectl apply -f k8s/inventory-virtualservice.yaml
	kubectl apply -f k8s/consume-service.yaml
	kubectl apply -f k8s/consume-virtualservice.yaml
	kubectl apply -f k8s/restock-service.yaml
	kubectl apply -f k8s/restock-virtualservice.yaml
	kubectl create namespace keycloak
	helm install keycloak bitnami/keycloak --set readinessProbe.enabled="false" --set livenessProbe.enabled="false" --set proxy="edge" --set httpRelativePath="/auth" --set auth.adminUser=admin --set auth.adminPassword=secret --namespace keycloak

	kubectl apply -f k8s/keycloak-virtualservice.yaml
	kubectl create namespace monitoring
	helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

