.PHONY: all build deploy

all: build deploy

build:
	docker build -t consume-service:latest -f services/consume/Dockerfile .
	docker build -t restock-service:latest -f services/restock/Dockerfile .
	docker build -t inventory-service:latest -f services/inventory/Dockerfile .
	kind load docker-image consume-service:latest --name istio-mono
	kind load docker-image restock-service:latest --name istio-mono
	kind load docker-image inventory-service:latest --name istio-mono

deploy:
	kubectl apply -f k8s/gateway.yaml
	kubectl apply -f k8s/inventory-service.yaml
	kubectl apply -f k8s/consume-service.yaml
	kubectl apply -f k8s/consume-virtualservice.yaml
	kubectl apply -f k8s/restock-service.yaml
	kubectl apply -f k8s/restock-virtualservice.yaml
