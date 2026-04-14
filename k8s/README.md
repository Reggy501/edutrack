# Kubernetes Deployment — Milestone 10

Deploy the entire EduTrack microservices architecture to AWS EKS.

## 📋 Prerequisites

1. **AWS Account** with EKS cluster running
2. **kubectl** installed and configured
3. **Docker images** built (from CI/CD pipeline)
4. **EKS Cluster** already deployed (via Terraform)

## 🚀 Quick Deploy (One Command)

```bash
cd k8s
chmod +x deploy.sh
./deploy.sh
```

This script will:
- Create `edutrack` namespace
- Deploy all 5 microservices (2 replicas each)
- Configure environment variables
- Set up services and ingress
- Wait for all pods to be ready
- Show you the access endpoint

---

## 📦 What Gets Deployed

| Service | Replicas | CPU | Memory | Port |
|---------|----------|-----|--------|------|
| auth-service | 2 | 250m | 256Mi | 8000 |
| student-service | 2 | 250m | 256Mi | 8000 |
| attendance-service | 2 | 250m | 256Mi | 8000 |
| grades-service | 2 | 250m | 256Mi | 8000 |
| notification-service | 2 | 250m | 256Mi | 8000 |

**Total Resources:** 5 services × 2 replicas = 10 pods running on t3.small nodes

---

## 🔧 Manual Deployment (Step by Step)

### Step 1: Create Namespace
```bash
kubectl apply -f namespace.yaml
```

### Step 2: Create Secrets & ConfigMaps
```bash
kubectl apply -f config.yaml
```

### Step 3: Deploy Services
```bash
kubectl apply -f auth-service.yaml
kubectl apply -f student-service.yaml
kubectl apply -f attendance-service.yaml
kubectl apply -f grades-service.yaml
kubectl apply -f notification-service.yaml
```

### Step 4: Deploy Ingress
```bash
kubectl apply -f ingress.yaml
```

### Step 5: Verify Deployment
```bash
# Check pods
kubectl get pods -n edutrack

# Check services
kubectl get svc -n edutrack

# Check ingress
kubectl get ingress -n edutrack

# Watch rollout
kubectl rollout status deployment/auth-service -n edutrack
```

---

## 🧪 Testing Your Deployment

### Port Forward to a Service
```bash
# Access auth-service locally
kubectl port-forward svc/auth-service 8000:8000 -n edutrack

# Now test at http://localhost:8000
```

### Check Service Logs
```bash
# View logs from a pod
kubectl logs -f pod/auth-service-xxxxx -n edutrack

# View logs from entire deployment
kubectl logs -f deployment/auth-service -n edutrack
```

### Describe Issues
```bash
# Get detailed pod info
kubectl describe pod auth-service-xxxxx -n edutrack

# Get events
kubectl get events -n edutrack
```

### Access the Ingress
```bash
# Get the load balancer DNS
kubectl get ingress -n edutrack

# Example output:
# NAME               CLASS   HOSTS   ADDRESS                        PORTS
# edutrack-ingress   alb     *       k8s-edutra-xxxxxxx.elb.amazonaws.com   80

# Now test:
curl http://k8s-edutra-xxxxxxx.elb.amazonaws.com/api/auth/
```

---

## 🔍 Understanding the Manifests

### Deployment (`*-service.yaml`)
Each service has:
- **2 replicas** for high availability
- **Resource requests** (minimum guaranteed)
- **Resource limits** (maximum allowed)
- **Liveness probe** (restarts if unhealthy)
- **Readiness probe** (removes from load balancer if failing)
- **Environment variables** from ConfigMap/Secrets

### Service
- **ClusterIP** type (internal service discovery)
- **Port 8000** (Django default)
- Enables service-to-service communication

### ConfigMap & Secret
- **ConfigMap**: Non-sensitive config (Django settings, hosts)
- **Secret**: Sensitive data (DB password, Django secret key)
- All services reference these centrally

### Ingress
- **AWS ALB** (Application Load Balancer)
- **Path-based routing** (`/api/auth`, `/api/students`, etc.)
- **Single DNS endpoint** for all services

---

## 📊 Monitoring

### Real-time Pod Status
```bash
watch kubectl get pods -n edutrack
```

### Pod Resource Usage
```bash
kubectl top pods -n edutrack
```

### Deployment Status
```bash
kubectl get deployments -n edutrack -o wide
```

### Network Policies
```bash
kubectl get networkpolicies -n edutrack
```

---

## 🛑 Cleanup (Stop AWS Charges!)

### Remove All Kubernetes Resources
```bash
kubectl delete namespace edutrack
# This deletes all pods, services, deployments, configmaps, secrets, etc.
```

### Destroy Infrastructure
After you're done testing, destroy AWS resources:
```bash
cd ../terraform
terraform destroy -lock=false
# Type 'yes' when prompted
```

---

## 📈 Scaling

### Scale a Deployment
```bash
# Scale auth-service to 5 replicas
kubectl scale deployment auth-service --replicas=5 -n edutrack
```

### Auto-scale (Requires Metrics Server)
```bash
# Create autoscale policy
kubectl autoscale deployment auth-service --min=2 --max=10 --cpu-percent=80 -n edutrack
```

---

## 🔐 Security Notes

⚠️ **THIS SETUP IS FOR DEMO ONLY** — Not production-grade security:

- Secrets are hardcoded in YAML (use AWS Secrets Manager in production)
- No network policies (open communication between all pods)
- No pod security policies
- Ingress has no TLS/HTTPS
- ImagePullPolicy=Always (requires image in registry)

**For production, implement:**
- [ ] AWS ECS/EKS Secrets Manager integration
- [ ] Network policies (deny-all by default)
- [ ] Pod Security Policies (PSP)
- [ ] TLS/HTTPS with ACM certificates
- [ ] Private container registry (ECR)
- [ ] RBAC (role-based access control)
- [ ] Resource quotas and limits

---

## 🆘 Troubleshooting

### Pods stuck in "Pending"
```bash
kubectl describe node
# Check if nodes have available CPU/memory
```

### Pods stuck in "CrashLoopBackOff"
```bash
kubectl logs -f pod/auth-service-xxxxx -n edutrack
# Check for Django errors
```

### Ingress not getting DNS
```bash
# Takes 2-3 minutes to provision ALB
kubectl describe ingress edutrack-ingress -n edutrack
```

### Can't connect to database
```bash
# Verify RDS endpoint and password in config.yaml
# Check security groups allow access from EKS nodes
```

---

## ✅ Success Checklist

- [ ] All 5 services deployed
- [ ] All 10 pods running (2 per service)
- [ ] Services can communicate (test inter-pod calls)
- [ ] Ingress endpoint responds to requests
- [ ] Logs show no errors
- [ ] Can port-forward and access locally
- [ ] Tested at least one API endpoint

---

## 📚 Next Steps

After deployment:

1. **Demo the System** — Show working microservices
2. **Test APIs** — Verify inter-service communication
3. **Monitor Metrics** — Check CPU/memory usage
4. **Take Screenshots** — For your portfolio
5. **Destroy Infrastructure** — Stop AWS charges

---

**Cost Estimate:** $0.50/hour while running (~$5-8/day)
**Deployment Time:** 3-5 minutes
**Interview Value:** ⭐⭐⭐⭐⭐ AMAZING demo of production-ready architecture
