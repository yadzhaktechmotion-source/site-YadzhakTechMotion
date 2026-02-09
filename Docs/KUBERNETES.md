# Kubernetes Migration Plan

---

## Target

- EKS (recommended)
- Managed Postgres (RDS)
- Managed Redis (optional)

---

## Migration Phases

1. Prepare container images
2. Deploy ingress + cert-manager
3. Externalize secrets
4. Deploy workloads
5. Gradual traffic cutover
6. Enable GitOps

---

## Benefits

- Auto-scaling
- Self-healing
- Better observability
