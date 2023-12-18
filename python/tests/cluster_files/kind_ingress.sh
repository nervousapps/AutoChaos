kind delete cluster

kind create cluster --config ~/AutoChaos/python/tests/cluster_files/kind_config.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

kubectl apply -f ~/AutoChaos/python/tests/cluster_files/deployment.yaml