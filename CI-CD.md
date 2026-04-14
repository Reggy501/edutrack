# CI/CD Pipeline — Milestone 9

Complete automated testing, building, and deployment pipeline using GitHub Actions.

## 📋 Workflows Overview

### 1. **Backend CI/CD** (`.github/workflows/ci-cd.yml`)
Runs on every push to `main` and `develop`, and on pull requests.

**Stages:**
- ✅ **Unit Tests** — Each microservice (auth, attendance, grades, notification, student) runs pytest
- 🐳 **Docker Build** — All 5 services build as Docker images after tests pass
- 🧪 **Integration Tests** — Services start with docker-compose and test inter-service communication
- 📤 **Docker Hub Push** — (Optional) Push images to your Docker Hub registry on main branch

### 2. **Frontend CI/CD** (`.github/workflows/frontend-ci.yml`)
Runs on pushes/PRs that touch `frontend/` directory.

**Stages:**
- 📦 Install dependencies
- 🔍 Run ESLint (linter)
- ✅ Run Jest tests
- 🏗️ Build production bundle
- 📊 Upload coverage reports

---

## 🚀 Quick Start

### Step 1: Push to GitHub
```bash
cd /media/reagan/54340941-6b55-4f54-bc28-c8e98acf6430/home/reagan/projects/edutrack
git add .github/
git commit -m "Milestone 9: Add GitHub Actions CI/CD pipeline"
git push origin main
```

### Step 2: Watch the Build
1. Go to your GitHub repo → **Actions** tab
2. Click the workflow run that just started
3. Watch each stage execute in real-time

---

## 🐳 Optional: Push to Docker Hub

To automatically push Docker images to Docker Hub on successful builds:

### Step 1: Create Docker Hub Account
1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up (free)
3. Create a **Personal Access Token** (Settings → Security → New Access Token)
4. Copy the token

### Step 2: Add GitHub Secrets
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add two secrets:
   - `DOCKER_USERNAME` — Your Docker Hub username
   - `DOCKER_PASSWORD` — Your Personal Access Token (NOT your password)

### Step 3: Images Will Auto-Push
After a successful build on `main` branch, images are pushed to:
- `yourusername/auth-service:latest`
- `yourusername/attendance-service:latest`
- `yourusername/grades-service:latest`
- `yourusername/notification-service:latest`
- `yourusername/student-service:latest`

---

## 🧪 What Each Workflow Tests

### Backend Services
Each service runs:
```bash
pytest tests/ -v
```

Tests must be in `{service}/tests/` directory.

### Integration Tests
Docker Compose starts all services + databases, then verifies:
- Services are healthy (port checks)
- Services can communicate
- Health endpoints respond correctly

### Frontend
- **Linter** — ESLint checks code style
- **Tests** — Jest unit tests  
- **Build** — Next.js/React production build
- **Coverage** — Code coverage reports

---

## 📊 Monitoring Builds

### In GitHub
1. **Actions** tab → See all workflow runs
2. Click a run → See real-time logs
3. Click a step → See detailed output

### Local Testing
Test locally before pushing:
```bash
# Test a single service
cd auth-service
pytest tests/ -v

# Test with docker-compose
docker-compose up -d
docker-compose exec auth-service pytest tests/ -v
docker-compose down

# Test frontend
cd frontend
npm test
```

---

## 🔄 Workflow Triggers

| Event | Trigger |
|-------|---------|
| Push to `main` or `develop` | Run full CI/CD |
| Pull Request | Run tests only (no push to registry) |
| Frontend file changes | Run frontend CI only (not backends) |

---

## ✅ Checklist After Setup

- [ ] Committed `.github/workflows/ci-cd.yml`
- [ ] Committed `.github/workflows/frontend-ci.yml`
- [ ] Pushed to GitHub
- [ ] Watched first workflow run in Actions tab
- [ ] All tests passed ✅
- [ ] Docker images built successfully
- [ ] (Optional) Set up Docker Hub secrets and verified image push

---

## 🆘 Troubleshooting

### Tests failing in CI but pass locally?
- Check Python/Node versions match
- Ensure all dependencies in `requirements.txt` or `package.json`
- Database credentials in test environment

### Docker build failing?
- Verify `Dockerfile` exists in each service directory
- Check Docker build context references correct paths
- Ensure `requirements.txt` is in the service root

### Integration tests timing out?
- Services may need more startup time
- Increase `sleep` duration in workflow
- Check docker-compose healthchecks

---

## 📚 Next Steps

After CI/CD is working:
1. **Add code coverage thresholds** (fail if coverage drops)
2. **Set up SonarQube** for code quality analysis
3. **Add security scanning** (Trivy for Docker images)
4. **Deploy to Kubernetes** (use images from Docker Hub)
5. **Set branch protection rules** (require passing tests before merge)

---

**Status:** ✅ Fully automated testing & building
**Cost:** 🎉 FREE (GitHub Actions includes free minutes)
**Interview Value:** ⭐⭐⭐⭐⭐ Demonstrates real DevOps automation
