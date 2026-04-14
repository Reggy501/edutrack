# EduTrack - Microservices Education Platform

A **production-grade microservices architecture** demonstrating full-stack DevOps, containerization, orchestration, and CI/CD automation.

[![GitHub Stars](https://img.shields.io/github/stars/Reggy501/edutrack?style=flat-square)](https://github.com/Reggy501/edutrack)
[![Last Commit](https://img.shields.io/github/last-commit/Reggy501/edutrack?style=flat-square)](https://github.com/Reggy501/edutrack)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

---

## 🎯 Project Overview

EduTrack is a **5-service microservices platform** built with Django REST Framework, deployed on **AWS EKS with Kubernetes**, automated via **GitHub Actions CI/CD**, and provisioned with **Terraform Infrastructure-as-Code**.

### Key Features

✅ **5 Independent Microservices**
- Authentication Service (JWT tokens)
- Student Management (CRUD operations)
- Attendance Tracking (real-time updates)
- Grades Management (academic records)
- Notification Service (email/SMS)

✅ **Production-Ready DevOps Stack**
- Docker containerization
- Kubernetes orchestration (EKS)
- Terraform infrastructure provisioning
- GitHub Actions CI/CD pipeline
- AWS RDS PostgreSQL database

✅ **High Availability**
- 2 replica pods per service (10 total)
- Load balancing with AWS ALB
- Service discovery with Kubernetes DNS
- Health checks & auto-restart

✅ **Automated Testing & Building**
- Unit tests on every commit
- Integration tests with docker-compose
- Automated Docker image building
- Frontend tests (React/Jest)

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  GitHub (CI/CD)                         │
│         GitHub Actions - automated testing              │
└──────────────────────┬──────────────────────────────────┘
                       │ git push
┌──────────────────────▼──────────────────────────────────┐
│              AWS EKS (Kubernetes)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  10 Pods (2 replicas × 5 services)               │  │
│  │  • auth-service                                  │  │
│  │  • student-service                               │  │
│  │  │  • attendance-service                         │  │
│  │  • grades-service                                │  │
│  │  • notification-service                          │  │
│  └──────────────────┬───────────────────────────────┘  │
│                    │                                    │
│  ┌─────────────────▼────────────────────────────┐      │
│  │   AWS ALB (Load Balancer)                    │      │
│  │   Routes /api/* to services                  │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │  AWS RDS PostgreSQL                          │      │
│  │  Shared by all 5 services                    │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘

All provisioned with Terraform Infrastructure-as-Code
Deployed via kubectl Kubernetes manifests
Tested automatically with GitHub Actions
```

---

## 🚀 Quick Start

### Deploy to AWS EKS (20 minutes)

```bash
# 1. Deploy infrastructure
cd terraform
terraform apply -lock=false

# 2. Connect kubectl
aws eks update-kubeconfig --region eu-north-1 --name edutrack-cluster

# 3. Deploy services
cd ../k8s
./deploy.sh

# 4. Get load balancer DNS
kubectl get ingress -n edutrack
```

**See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guide.**

### Local Development

```bash
# Install dependencies
cd auth-service
pip install -r requirements.txt

# Set Django settings
export DJANGO_SETTINGS_MODULE=config.settings

# Run tests
pytest tests/ -v

# Start service locally
python manage.py runserver 0.0.0.0:8000
```

---

## 📁 Project Structure

```
edutrack/
├── .github/workflows/           # GitHub Actions CI/CD
│   ├── ci-cd.yml               # Backend microservices testing & Docker build
│   └── frontend-ci.yml         # Frontend React testing & building
│
├── auth-service/               # Authentication microservice
│   ├── authentication/         # Django app
│   ├── config/                 # Django settings
│   ├── tests/                  # Unit tests
│   ├── Dockerfile              # Container image
│   ├── requirements.txt        # Python dependencies
│   └── manage.py
│
├── student-service/            # Student management microservice
├── attendance-service/         # Attendance tracking microservice
├── grades-service/             # Grades management microservice
├── notification-service/       # Notification microservice
│
├── terraform/                  # AWS Infrastructure as Code
│   ├── main.tf                 # Main stack
│   ├── vpc.tf                  # Network (VPC, subnets)
│   ├── eks.tf                  # Kubernetes (EKS cluster, node groups)
│   ├── rds.tf                  # Database (PostgreSQL)
│   ├── iam.tf                  # Permissions and roles
│   ├── security_groups.tf      # Firewall rules
│   ├── variables.tf            # Configuration parameters
│   ├── outputs.tf              # Output values
│   └── terraform.tfstate       # State file (tracks AWS resources)
│
├── k8s/                        # Kubernetes deployment manifests
│   ├── namespace.yaml          # Create edutrack namespace
│   ├── config.yaml             # ConfigMaps & Secrets
│   ├── auth-service.yaml       # Auth service deployment
│   ├── student-service.yaml    # Student service deployment
│   ├── attendance-service.yaml # Attendance service deployment
│   ├── grades-service.yaml     # Grades service deployment
│   ├── notification-service.yaml # Notification service deployment
│   ├── ingress.yaml            # AWS ALB load balancer routing
│   ├── deploy.sh               # One-command deployment script
│   └── README.md               # K8s deployment guide
│
├── frontend/                   # React frontend (not deployed in K8s)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── docker-compose.yml          # Local development (all services + databases)
├── DEPLOYMENT.md               # Detailed AWS deployment guide
├── CI-CD.md                    # GitHub Actions automation guide
└── README.md                   # This file
```

---

## 🛠 Technology Stack

### Backend
- **Framework:** Django REST Framework (Python)
- **Database:** PostgreSQL 15
- **APIs:** RESTful with JWT authentication
- **Testing:** pytest with coverage

### Infrastructure
- **Cloud:** AWS (EKS, RDS, VPC, ALB, IAM)
- **Orchestration:** Kubernetes (1.30)
- **IaC:** Terraform
- **Containerization:** Docker

### DevOps & Automation
- **CI/CD:** GitHub Actions
- **Version Control:** Git & GitHub
- **Container Registry:** Docker Hub (optional)

### Frontend
- **Framework:** React
- **Testing:** Jest
- **Build:** npm/webpack
- **Deployment:** (Static hosting - not in this project)

---

## 📈 Features

### Microservices Design
- **Independent Services** — Each service has its own database tables
- **REST APIs** — Easy service-to-service communication
- **Scalability** — Scale services individually
- **Resilience** — Failure of one service doesn't crash others

### High Availability
- **Pod Replication** — 2 replicas per service ensure availability
- **Load Balancing** — AWS ALB distributes traffic
- **Health Checks** — Kubernetes auto-restarts failed pods
- **Rolling Updates** — Zero-downtime deployments

### Automated Testing
- **Unit Tests** — pytest for all Django services
- **Integration Tests** — Services tested together
- **Code Quality** — Automated linting & formatting
- **Frontend Tests** — Jest for React components

### Infrastructure as Code
- **Reproducible** — Deploy identical environments
- **Version Controlled** — Track infrastructure changes in git
- **Readable** — Terraform makes infrastructure explicit
- **Safe** — Plan before applying changes

---

## 📊 Observability

### Monitoring

View pod status:
```bash
kubectl get pods -n edutrack
```

Check service logs:
```bash
kubectl logs -f deployment/auth-service -n edutrack
```

Port forward for local testing:
```bash
kubectl port-forward svc/auth-service 8000:8000 -n edutrack
```

### Metrics

```bash
# Pod resource usage
kubectl top pods -n edutrack

# Node resource usage
kubectl top nodes
```

---

## 💰 Cost Analysis

### Minimal Deployment (Demo)
- **EKS Cluster:** $0.10/hour (control plane)
- **2 × t3.small nodes:** $0.046/hour
- **RDS PostgreSQL:** $0.17/hour (single-AZ, free tier)
- **NAT Gateway + ALB:** $0.061/hour

**Total: ~$0.39/hour (~$9/day, ~$270/month)**

### Cost Optimization
- ✅ t3.small nodes (30% cheaper than t3.medium)
- ✅ Single-AZ RDS (half the cost of multi-AZ)
- ✅ On-demand pricing (no reserved instances)
- ✅ EBS optimization disabled where possible

### Saving Money
```bash
# Destroy infrastructure (stop all charges)
terraform destroy -lock=false
kubectl delete namespace edutrack
```

---

## 🔒 Security

### Current (Demo)
✅ JWT authentication
✅ Docker image isolation
✅ AWS security groups
✅ PostgreSQL password protection

### For Production, Add:
- [ ] HTTPS/TLS with AWS ACM
- [ ] AWS Secrets Manager for sensitive data
- [ ] Network policies (deny-all default)
- [ ] Pod security policies
- [ ] RBAC (role-based access control)
- [ ] Audit logging
- [ ] Container image scanning
- [ ] Rate limiting on APIs

---

## 📚 Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** — Step-by-step AWS deployment guide
- **[CI-CD.md](./CI-CD.md)** — GitHub Actions workflows explained
- **[k8s/README.md](./k8s/README.md)** — Kubernetes manifests guide
- **[terraform/README.md](./terraform/README.md)** — Infrastructure code docs

---

## 👨‍💻 Development

### Run Locally with Docker Compose

```bash
# Start all services and databases
docker-compose up -d

# Wait for services to be healthy
docker-compose ps

# Run tests
docker-compose exec auth-service pytest tests/ -v

# View logs
docker-compose logs -f auth-service

# Tear down
docker-compose down -v
```

### Run Tests Locally

```bash
cd auth-service
export DJANGO_SETTINGS_MODULE=config.settings
pytest tests/ -v --cov
```

### Build Docker Images

```bash
docker build -t edutrack/auth-service:latest ./auth-service
docker build -t edutrack/student-service:latest ./student-service
# ... repeat for other services
```

---

## 🚀 Deployment Strategies

### Development (Local)
```bash
docker-compose up
# All services on localhost
```

### Staging/Production (EKS)
```bash
terraform apply
# AWS infrastructure
kubectl apply -f k8s/
# Kubernetes services
```

### Blue-Green Deployments
Kubernetes handles rolling updates automatically:
```bash
kubectl set image deployment/auth-service \
  auth-service=edutrack/auth-service:v2.0 \
  -n edutrack
```

### Canary Deployments
Start with 1 replica, gradually increase:
```bash
kubectl scale deployment auth-service --replicas=1 -n edutrack
# Test new version...
kubectl scale deployment auth-service --replicas=2 -n edutrack
```

---

## 🎓 Learning Outcomes

By studying this project, you'll understand:

✅ **Microservices Architecture**
- How to split monolith into services
- Inter-service communication (REST APIs)
- Database per service pattern
- Eventual consistency

✅ **Container Orchestration**
- Kubernetes core concepts (pods, deployments, services)
- Health checks & auto-scaling
- Rolling updates & rollbacks
- Resource management

✅ **Infrastructure as Code**
- Terraform syntax & workflow
- AWS resource provisioning
- State management
- Modules & reusability

✅ **CI/CD Automation**
- GitHub Actions workflows
- Automated testing
- Docker image building
- Multi-environment deployments

✅ **DevOps Best Practices**
- Version control for infrastructure
- Reproducible deployments
- Monitoring & observability
- Cost optimization

---

## 🤝 Contributing

This is a **learning project**. Feel free to:
- ✅ Fork and modify for your own learning
- ✅ File issues if you find bugs
- ✅ Submit PRs with improvements
- ✅ Use as portfolio piece

---

## 📋 Project Roadmap

### Completed ✅
- [x] 5 microservices with REST APIs
- [x] PostgreSQL database
- [x] Docker containerization
- [x] Kubernetes deployment manifests
- [x] Terraform infrastructure code
- [x] GitHub Actions CI/CD
- [x] Complete documentation

### Future Enhancements
- [ ] Service mesh (Istio)
- [ ] Distributed tracing (Jaeger)
- [ ] API Gateway (Kong)
- [ ] GraphQL API layer
- [ ] Frontend deployment (React on S3 + CloudFront)
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Logging (ELK stack)
- [ ] Private container registry (ECR)

---

## ✨ Interview Talking Points

When discussing this project:

**Architecture:**
> "I designed a microservices architecture with 5 independent services communicating via REST APIs. Each service has its own codebase, can be deployed independently, and scales horizontally."

**DevOps:**
> "I automated the entire deployment pipeline with Terraform to provision AWS infrastructure and Kubernetes for container orchestration, making deployment repeatable and version-controlled."

**CI/CD:**
> "I implemented GitHub Actions to automatically test code, build Docker images, and run integration tests on every commit, ensuring code quality at scale."

**Problem Solving:**
> "I faced challenges with database isolation, service communication, and Kubernetes networking, which I solved by implementing circuit breakers, health checks, and service discovery."

---

## 🆘 Troubleshooting

Common issues and solutions:

**Docker build fails:**
```bash
# Clear Docker cache
docker system prune -af
docker build --no-cache -t edutrack/auth-service:latest ./auth-service
```

**Kubectl commands timeout:**
```bash
# Check cluster is accessible
kubectl cluster-info
aws eks describe-cluster --name edutrack-cluster --region eu-north-1
```

**Pods stuck in pending:**
```bash
# Check node resources
kubectl describe node
# Check pod events
kubectl describe pod POD_NAME -n edutrack
```

**Database connection errors:**
```bash
# Verify RDS is accessible
psql -h ENDPOINT -U postgres -d edutrack_auth
# Check security groups allow traffic
```

---

## 📞 Contact & Resources

- **GitHub:** https://github.com/Reggy501/edutrack
- **AWS Docs:** https://docs.aws.amazon.com/
- **Kubernetes Docs:** https://kubernetes.io/docs/
- **Terraform Docs:** https://www.terraform.io/docs/

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🎉 Congratulations!

You've reviewed a **production-grade microservices architecture**. This demonstrates:

⭐ Advanced DevOps & Infrastructure knowledge
⭐ Cloud architecture design (AWS)
⭐ Container orchestration (Kubernetes)
⭐ Infrastructure automation (Terraform)
⭐ CI/CD pipeline design (GitHub Actions)
⭐ Microservices best practices

**Perfect for senior DevOps engineer interviews.**

---

**Last Updated:** April 14, 2026
**Version:** 1.0.0
**Maintainer:** [Reagan](https://github.com/Reggy501)
