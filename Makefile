.PHONY: all build deploy

all: build deploy

delete:
	kind delete clusters istio-mono
	
build:
	sh ./scripts/create_kind_cluster.sh
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	cd services/consume && docker build -t consume-service:latest .
	cd services/restock && docker build -t restock-service:latest .
	cd services/inventory && docker build -t inventory-service:latest .
	cd services/hello && docker build -t hello-service:latest .
	kind load docker-image consume-service:latest --name istio-mono
	kind load docker-image restock-service:latest --name istio-mono
	kind load docker-image inventory-service:latest --name istio-mono
	kind load docker-image hello-service:latest --name istio-mono

deploy:
	kubectl apply -f k8s/gateway.yaml
	kubectl apply -f k8s/inventory-service.yaml
	kubectl apply -f k8s/inventory-virtualservice.yaml
	kubectl apply -f k8s/consume-service.yaml
	kubectl apply -f k8s/consume-virtualservice.yaml
	kubectl apply -f k8s/restock-service.yaml
	kubectl apply -f k8s/restock-virtualservice.yaml
	kubectl apply -f k8s/hello-service.yaml
	kubectl apply -f k8s/hello-virtualservice.yaml
	kubectl create namespace keycloak
	helm install keycloak bitnami/keycloak --set readinessProbe.enabled="true" --set livenessProbe.enabled="true" --set proxy="edge" --set httpRelativePath="/auth/" --set auth.adminUser=admin --set auth.adminPassword=secret --namespace keycloak
	kubectl apply -f k8s/keycloak-virtualservice.yaml
	kubectl apply -f k8s/keycloak-config-job.yaml
	kubectl create namespace monitoring
	helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

