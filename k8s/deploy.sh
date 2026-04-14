#!/bin/bash
# EduTrack Kubernetes Deployment Script
# Deploys all services to EKS cluster

set -e

echo "🚀 EduTrack Kubernetes Deployment"
echo "=================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Install it first."
    exit 1
fi

# Check cluster connection
echo "✅ Checking cluster connection..."
kubectl cluster-info
echo ""

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f k8s/namespace.yaml
sleep 2

# Apply config and secrets
echo "⚙️  Applying configuration..."
kubectl apply -f k8s/config.yaml
sleep 2

# Deploy all services
echo "🐳 Deploying microservices..."
kubectl apply -f k8s/auth-service.yaml
echo "   ✅ Auth service deployed"

kubectl apply -f k8s/student-service.yaml
echo "   ✅ Student service deployed"

kubectl apply -f k8s/attendance-service.yaml
echo "   ✅ Attendance service deployed"

kubectl apply -f k8s/grades-service.yaml
echo "   ✅ Grades service deployed"

kubectl apply -f k8s/notification-service.yaml
echo "   ✅ Notification service deployed"

sleep 3

# Deploy ingress
echo "🌐 Deploying ingress..."
kubectl apply -f k8s/ingress.yaml
sleep 3

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Checking pod status..."
kubectl get pods -n edutrack

echo ""
echo "🔗 Services:"
kubectl get svc -n edutrack

echo ""
echo "⏳ Waiting for pods to be ready (this may take 1-2 minutes)..."
kubectl rollout status deployment/auth-service -n edutrack --timeout=5m
kubectl rollout status deployment/student-service -n edutrack --timeout=5m
kubectl rollout status deployment/attendance-service -n edutrack --timeout=5m
kubectl rollout status deployment/grades-service -n edutrack --timeout=5m
kubectl rollout status deployment/notification-service -n edutrack --timeout=5m

echo ""
echo "🎉 All services are running!"
echo ""
echo "📍 Ingress endpoint:"
kubectl get ingress -n edutrack

echo ""
echo "💡 Try these commands to test:"
echo "   kubectl logs -f deployment/auth-service -n edutrack"
echo "   kubectl port-forward svc/auth-service 8000:8000 -n edutrack"
echo ""
echo "⏹️  To tear down: kubectl delete namespace edutrack"
