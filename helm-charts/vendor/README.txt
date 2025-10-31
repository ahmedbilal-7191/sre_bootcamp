helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd


# argocd-values.yaml
global:
  domain: ""
  nodeSelector:
    type: services_d

# Individual component configurations
controller:
  nodeSelector:
    type: services_d

server:
  nodeSelector:
    type: services_d
  service:
    type: ClusterIP  # Change to LoadBalancer if you want external access
    ports:
      https: 443

repoServer:
  nodeSelector:
    type: services_d

redis:
  nodeSelector:
    type: services_d

dex:
  nodeSelector:
    type: services_d

applicationSet:
  nodeSelector:
    type: services_d



helm install argocd argo/argo-cd \
  -n argocd \
  -f argocd-values.yaml




kubectl get pods -n argocd -o wide
