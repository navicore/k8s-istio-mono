#!/usr/bin/env bash

curl -X POST http://172.18.0.5/restock -H "Content-Type: application/json" -d '{"sku": "12345", "quantity": 20}'
