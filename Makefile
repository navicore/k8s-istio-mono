.PHONY: all build deploy

all: build deploy

build:
	docker build -t consume-service:latest -f services/consume/Dockerfile .
	docker build -t restock-service:latest -f services/restock/Dockerfile .
	docker build -t inventory-service:latest -f services/inventory/Dockerfile .

deploy:
	kubectl apply -f k8s/consume-service.yaml
	kubectl apply -f k8s/restock-service.yaml
	kubectl apply -f k8s/inventory-service.yaml
