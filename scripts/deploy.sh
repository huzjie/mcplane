#!/usr/bin/env bash
set -euo pipefail

echo "==> Building Docker image"
docker build -t mcplane:latest .

echo "==> Deploying to Kubernetes"
kubectl apply -f k8s/

echo "==> Done"
