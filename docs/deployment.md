# 部署

## Docker

```bash
docker build -t mcplane .
docker run -p 8090:8090 mcplane
```

## Kubernetes

```bash
kubectl apply -f k8s/
```

## Helm

```bash
helm install mcplane ./helm/mcplane
```
