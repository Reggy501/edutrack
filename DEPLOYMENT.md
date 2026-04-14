# EduTrack Deployment Guide

Complete guide to deploying the EduTrack microservices architecture on AWS EKS.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Cost Estimates](#cost-estimates)
7. [Cleanup](#cleanup)

---

## 🚀 Quick Start

Deploy the entire stack in 3 commands:

```bash
# 1. Deploy AWS infrastructure (takes ~20 minutes)
cd terraform
terraform apply -lock=false

# 2. Connect kubectl to EKS cluster
aws eks update-kubeconfig --region eu-north-1 --name edutrack-cluster
kubectl get nodes

# 3. Deploy Kubernetes services
cd ../k8s
chmod +x deploy.sh
./deploy.sh
```

That's it! Your entire system is live.

---

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Region: eu-north-1                │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │              VPC (10.0.0.0/16)                   │  │
│  │                                                  │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │         AWS EKS Cluster                    │ │  │
│  │  │  Kubernetes 1.30 (2 t3.small nodes)       │ │  │
│  │  │                                            │ │  │
│  │  │  ┌────────┐  ┌────────┐  ┌────────┐      │ │  │
│  │  │  │ Auth   │  │Student │  │Attend. │      │ │  │
│  │  │  │Service │  │Service │  │Service │  ... │ │  │
│  │  │  └────────┘  └────────┘  └────────┘      │ │  │
│  │  │      (2 replicas each)                    │ │  │
│  │  │                                            │ │  │
│  │  │  ┌───────────────────────────────────┐    │ │  │
│  │  │  │    AWS ALB (Load Balancer)        │    │ │  │
│  │  │  │  Routes /api/* to services        │    │ │  │
│  │  │  └───────────────────────────────────┘    │ │  │
│  │  └────────────────────────────────────────────┘ │  │
│  │                                                  │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │    RDS PostgreSQL Database 15.10           │ │  │
│  │  │    (Shared by all 5 services)              │ │  │
│  │  │    backup_retention: 0 days (free tier)    │ │  │
│  │  └────────────────────────────────────────────┘ │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Microservices (5 services, 2 replicas each)

| Service | Port | Purpose | Replicas |
|---------|------|---------|----------|
| auth-service | 8000 | User authentication & JWT | 2 |
| student-service | 8000 | Student management | 2 |
| attendance-service | 8000 | Attendance tracking | 2 |
| grades-service | 8000 | Grade management | 2 |
| notification-service | 8000 | Email/SMS notifications | 2 |

**Total:** 10 pods across 2 nodes

---

## ✅ Prerequisites

### Required
- **AWS Account** with `default` credentials configured
- **Terraform** v1.14+ installed
- **kubectl** v1.30+ installed
- **Docker** (for building images locally)
- **git** (code already cloned)

### Recommended
- **AWS CLI** v2 (for easier management)
- **12GB+ free disk space**
- **4GB+ RAM** on local machine

### Verify Installation

```bash
# Terraform
terraform version

# kubectl
kubectl version --client

# AWS credentials
aws sts get-caller-identity

# Docker
docker --version
```

---

## 📝 Step-by-Step Deployment

### Step 1: Deploy AWS Infrastructure (20 mins)

This creates: VPC, EKS cluster, RDS database, security groups, IAM roles.

```bash
cd terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy infrastructure
terraform apply -lock=false
# Type 'yes' when prompted
```

**What's happening:**
- VPC with public/private subnets created (2-3 min)
- NAT Gateway provisioned (3-5 min)
- EKS control plane launched (10-15 min) ⏳ **Longest step**
- EKS worker nodes added (3-5 min)
- RDS PostgreSQL instance created (3-5 min)

**Expected output:**
```
Apply complete! Resources: 27 added, 0 changed, 0 destroyed.

Outputs:
eks_cluster_endpoint = "https://xxxxxx.eks.eu-north-1.amazonaws.com"
eks_cluster_name = "edutrack-cluster"
rds_endpoint = "edutrack-db.xxxxx.rds.eu-north-1.amazonaws.com:5432"
vpc_id = "vpc-xxxxxx"
```

### Step 2: Configure kubectl (1 min)

Connect your local `kubectl` to the EKS cluster:

```bash
# Update kubeconfig
aws eks update-kubeconfig --region eu-north-1 --name edutrack-cluster

# Verify connection
kubectl cluster-info
kubectl get nodes

# Expected output:
# NAME                          STATUS   ROLES    AGE   VERSION
# ip-10-0-10-xxx.eu-north...    Ready    <none>   2m    v1.30.14-eks-xxx
# ip-10-0-11-xxx.eu-north...    Ready    <none>   2m    v1.30.14-eks-xxx
```

### Step 3: Build Docker Images (5-10 mins)

Build container images for all services:

```bash
docker build -t edutrack/auth-service:latest ./auth-service
docker build -t edutrack/student-service:latest ./student-service
docker build -t edutrack/attendance-service:latest ./attendance-service
docker build -t edutrack/grades-service:latest ./grades-service
docker build -t edutrack/notification-service:latest ./notification-service

# Verify images
docker images | grep edutrack
```

**Note:** In production, push these to ECR or Docker Hub, then reference them in Kubernetes manifests.

### Step 4: Deploy to Kubernetes (5 mins)

Deploy all services to EKS:

```bash
cd k8s

# Make script executable
chmod +x deploy.sh

# Deploy everything
./deploy.sh

# Watch deployment progress
kubectl get pods -n edutrack -w

# Expected to see all 10 pods transition to "Running"
# This takes 1-2 minutes as Docker downloads and starts images
```

**What the script does:**
1. Creates `edutrack` namespace
2. Applies ConfigMaps and Secrets
3. Deploys 5 services with 2 replicas each
4. Creates Kubernetes services for service discovery
5. Provisions AWS ALB (Application Load Balancer)
6. Waits for all pods to be healthy

### Step 5: Verify Deployment (3 mins)

Confirm everything is running:

```bash
# Check pods are running
kubectl get pods -n edutrack
# Expected: 10 pods in "Running" state

# Check services
kubectl get svc -n edutrack
# Expected: 5 ClusterIP services

# Check ingress (load balancer)
kubectl get ingress -n edutrack
# Expected: Load balancer DNS endpoint
```

### Step 6: Access Your Services

Get the load balancer endpoint:

```bash
# Get the DNS name
kubectl get ingress edutrack-ingress -n edutrack -o wide

# Example output:
# NAME               CLASS   HOSTS   ADDRESS                         PORTS
# edutrack-ingress   alb     *       k8s-edutra-abc123.elb.eu...     80

# Test the services:
INGRESS_DNS="k8s-edutra-abc123.elb.eu-north-1.amazonaws.com"

# Auth service
curl http://$INGRESS_DNS/api/auth/

# Student service
curl http://$INGRESS_DNS/api/students/

# Check service logs
kubectl logs -f deployment/auth-service -n edutrack
```

---

## 🔍 Monitoring & Troubleshooting

### Check Pod Status

```bash
# View all pods
kubectl get pods -n edutrack

# Detailed pod info
kubectl describe pod auth-service-xxxxx -n edutrack

# Pod logs
kubectl logs -f pod/auth-service-xxxxx -n edutrack

# Previous logs (if pod crashed and restarted)
kubectl logs --previous pod/auth-service-xxxxx -n edutrack
```

### Common Issues

**Pods stuck in "Pending":**
```bash
kubectl describe node
# Check available CPU/memory on nodes
```

**Pods in "CrashLoopBackOff":**
```bash
kubectl logs -f deployment/auth-service -n edutrack
# Check Django error messages
```

**Can't reach services:**
```bash
# Check security groups in AWS Console
# Verify ingress is provisioned
kubectl get ingress -n edutrack
```

**Pod memory/CPU issues:**
```bash
# Check resource usage
kubectl top pods -n edutrack

# See resource limits
kubectl describe pod auth-service-xxxxx -n edutrack
```

### Port Forward (Local Testing)

Access services locally without load balancer:

```bash
# Forward local port 8000 to auth-service
kubectl port-forward svc/auth-service 8000:8000 -n edutrack

# In another terminal, test locally
curl http://localhost:8000/api/auth/
```

---

## 💰 Cost Estimates

### Hourly Costs

| Component | Type | Cost/hour |
|-----------|------|-----------|
| EKS Cluster | Control plane | $0.10 |
| EC2 Nodes | 2× t3.small | $0.023 × 2 = $0.046 |
| RDS Database | PostgreSQL t4g.micro multi-AZ | $0.17 |
| NAT Gateway | Data processing | $0.045 |
| Load Balancer | ALB | $0.016 |
| **Total** | | **~$0.39/hour** |

### Daily/Monthly Costs
- **Per day:** ~$9.40
- **Per month:** ~$282

### Free Tier Eligibility
⚠️ **Not eligible:** EKS has no free tier (minimum $0.10/hour just for control plane)

---

## 🛑 Cleanup (Stop Charges!)

### Remove Kubernetes Resources

```bash
# Delete the namespace (removes all pods, services, ingress)
kubectl delete namespace edutrack

# Verify deletion
kubectl get namespaces
```

### Destroy AWS Infrastructure

```bash
cd terraform

# Preview what will be deleted
terraform plan -destroy

# Delete everything
terraform destroy -lock=false
# Type 'yes' when prompted
```

**What gets destroyed:**
- EKS cluster ✓
- RDS database ✓
- VPC, subnets, security groups ✓
- NAT gateway, elastic IP ✓
- IAM roles and policies ✓

---

## 📊 Architecture Decisions

### Why These Choices?

**EKS over ECS:**
- Industry standard container orchestration
- Better for learning Kubernetes
- More portable (can move to any K8s cluster)

**t3.small nodes:**
- Smallest general-purpose instances
- Minimum cost while supporting 5 services
- Enough for demo/testing (~2 GB memory per service)

**2 replicas per service:**
- High availability (pod failure doesn't down service)
- Load balancing
- Rolling updates without downtime

**RDS multi-AZ avoided:**
- Single-AZ for cost savings (demo only)
- Multi-AZ would add $0.15/hour

**PostgreSQL (not DynamoDB):**
- Services require relational data
- Familiar SQL interface
- ACID guarantees

---

## 🔐 Security Notes

⚠️ **This setup is for DEMO/LEARNING only** — not production-ready:

### Issues:
- Secrets hardcoded in YAML (should use AWS Secrets Manager)
- No TLS/HTTPS (exposed on HTTP)
- No pod security policies
- All-open security groups
- No network policies (all pods can talk to all pods)
- Images pulled with `imagePullPolicy: Always` (requires public registry)

### For Production, Add:
- [ ] TLS with ACM certificates
- [ ] AWS Secrets Manager integration
- [ ] Network policies (deny-all default)
- [ ] Pod security policies
- [ ] Private ECR for images
- [ ] RBAC role-based access control
- [ ] Audit logging
- [ ] Rate limiting on ingress
- [ ] Auto-scaling policies
- [ ] Data encryption at rest

---

## 📚 Related Documentation

- [CI/CD Pipeline](../CI-CD.md) — GitHub Actions workflows
- [Kubernetes Manifests](./README.md) — Detailed K8s configs
- [Infrastructure Code](../terraform/README.md) — Terraform modules
- [Microservices](../README.md) — Service documentation

---

## 🆘 Getting Help

### Check Logs
```bash
# Kubernetes events
kubectl get events -n edutrack

# Service logs
kubectl logs -f deployment/SERVICE_NAME -n edutrack
```

### AWS Console
- **EKS:** https://console.aws.amazon.com/eks/
- **RDS:** https://console.aws.amazon.com/rds/
- **VPC:** https://console.aws.amazon.com/vpc/
- **CloudWatch:** https://console.aws.amazon.com/cloudwatch/

### Useful Commands

```bash
# Full pod info
kubectl get pods -n edutrack -o wide

# Pod resource usage
kubectl top pods -n edutrack

# Service details
kubectl describe service auth-service -n edutrack

# Deployment rollout status
kubectl rollout status deployment/auth-service -n edutrack

# Scale a deployment
kubectl scale deployment auth-service --replicas=5 -n edutrack

# Port forward
kubectl port-forward svc/auth-service 8000:8000 -n edutrack
```

---

## ✅ Deployment Checklist

- [ ] AWS credentials configured
- [ ] Terraform installed and working
- [ ] kubectl installed
- [ ] Docker installed
- [ ] VPC + EKS deployed successfully
- [ ] RDS database accessible
- [ ] kubectl connected to cluster
- [ ] Docker images built
- [ ] Kubernetes manifests deployed
- [ ] All 10 pods running
- [ ] Ingress provisioned with DNS
- [ ] Services respond to HTTP requests
- [ ] Can see logs from pods
- [ ] Cleanup script tested

---

## 🎉 You Did It!

You've successfully deployed:
- ✅ 5 microservices
- ✅ 10 replicated pods
- ✅ Load-balanced ingress
- ✅ PostgreSQL database
- ✅ On **production-grade Kubernetes**

**Estimated time to deploy:** 25-30 minutes

**Cost:** ~$9.40/day while running, $0 after cleanup

**Interview value:** ⭐⭐⭐⭐⭐ **EXCEPTIONAL**

---

**Last updated:** April 14, 2026
**Version:** 1.0
