echNova Solutions — Containerized Application with Docker, Redis, Kubernetes and Jenkins CI/CD
1. Project Overview
TechNova Solutions is a containerized web application used to practise application deployment, container management, Kubernetes orchestration, and CI/CD automation.

The application consists of:
- A static frontend served by Nginx.
- A Python HTTP backend API.
- Redis for caching API responses.
The project supports Docker Compose for local or single-host deployment and Kubernetes for orchestrated deployment. Jenkins automates source-code checkout, Docker image builds, publishing to Docker Hub, Kubernetes deployment, and deployment verification.
2. Technology Stack
- Operating System: Linux (Ubuntu / RHEL)
- Container Runtime: Docker
- Container Orchestration: Docker Compose and Kubernetes
- CI/CD: Jenkins
- Frontend Web Server: Nginx
- Backend: Python 3.12
- Cache: Redis
- Frontend: HTML5 and CSS3
- Image Registry: Docker Hub
- Version Control: Git and GitHub
- Kubernetes Networking: Calico (cluster CNI); Nginx Ingress Controller
3. Application Architecture
The application has three main services:
1. Frontend: Nginx serves the static website and forwards API requests to the backend.
2. Backend: A Python HTTP API provides service information and a health endpoint.
3. Redis: Stores the service-information response with a 60-second expiration period.
The backend connects to Redis using the Kubernetes/Docker service hostname and port. In Kubernetes, the backend uses REDIS_HOST and REDIS_PORT_NUMBER environment variables.
Request flow
User Browser
     |
     | HTTP
     v
Nginx Frontend
     |
     | /api/*
     v
Python Backend API
     |
     | Redis protocol
     v
Redis Cache
Kubernetes service design
- frontend-service: ClusterIP service exposing the frontend on port 80.
- backend-service: ClusterIP service exposing the backend on port 5000.
- redis: ClusterIP service exposing Redis on port 6379.
- technova-ingress: Nginx Ingress resource for the host technova.local.
The backend and Redis are intended to communicate using Kubernetes service DNS. Backend and Redis ports do not need to be exposed externally.
4. Project Structure
The repository contains the application source, Docker configuration, Kubernetes manifests, and Jenkins pipeline.
technova-website/
├── frontend/
│   ├── Dockerfile
│   └── ...                 # Frontend application files
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── ...                 # Deployments, Services, Ingress and related manifests
├── Jenkinsfile
├── compose.yaml
├── nginx.conf
├── .dockerignore
└── README.md
The exact filenames under frontend/ and k8s/ depend on the manifests and source files committed to the repository.
5. Application Features
- Company website served by Nginx.
- Python backend API.
- Four service categories:
  - Cloud Computing
  - DevOps Automation
  - Linux Administration
  - Monitoring and Observability
- Redis caching with a 60-second TTL.
- Backend health endpoint at /health.
- Nginx reverse proxy for API requests.
- Separate frontend, backend, and Redis services.
- Docker images published to Docker Hub.
- Kubernetes Deployments, Services, and Ingress.
- Jenkins pipeline for build, image publishing, deployment, and verification.
6. API Endpoints
Endpoint	Purpose
/	Serves the website through Nginx
/api/services	Returns company information and the four services
/health	Returns backend health status


The backend's /api/services endpoint reads the technova:services key from Redis. A cache miss generates and stores the response for 60 seconds. A cache hit returns the cached response.

Example response:
{
  "company": "TechNova Solutions",
  "services": [
    "Cloud Computing",
    "DevOps Automation",
    "Linux Administration",
    "Monitoring and Observability"
  ],
  "cache": "HIT"
}
The cache field is included for cache-behavior demonstration.
7. Redis Configuration and Caching
The backend connects to Redis using these environment variables:
Variable	Example value	Purpose
REDIS_HOST	redis	Redis Service/container hostname
REDIS_PORT_NUMBER	6379	Redis TCP port
PORT	5000	Backend HTTP listening port


Important Kubernetes note: Kubernetes automatically creates service-related environment variables for Services. For a Service named redis, it may create REDIS_PORT with a value such as tcp://10.x.x.x:6379. Do not parse that value as an integer. The backend uses REDIS_PORT_NUMBER to avoid this naming conflict.
Cache behavior
- MISS: The key is not present; the backend creates the response and stores it in Redis.
- HIT: A valid cached response is returned.
- Expiration: The key expires after 60 seconds; a later request creates a new cache entry.
The backend returns HTTP 503 for /api/services if Redis is unavailable. The /health endpoint checks the HTTP application process and does not itself verify Redis connectivity.
8. Docker Configuration
Frontend
The frontend image uses Nginx to serve the website. Nginx forwards /api/ requests to the backend service.
Backend
The backend image uses Python 3.12 Slim. Its Dockerfile:
- Installs dependencies from requirements.txt.
- Copies app.py into /app.
- Creates and runs as a non-root user (10001).
- Exposes container port 5000.
Redis
Redis stores cached API responses. Cache entries expire after 60 seconds.
9. Docker Compose Deployment
Prerequisites
- Linux host with Docker installed.
- Docker Compose support.
- Git, if cloning the repository.
- Network access to the published frontend port.
Build and start
From the project root:
docker compose build
docker compose up -d
Check services and logs
docker compose ps
docker compose logs
For an individual service:
docker compose logs frontend
docker compose logs backend
docker compose logs redis
Access the website
If the Compose configuration publishes host port 8081, open:
http://YOUR_SERVER_IP:8081
Replace YOUR_SERVER_IP with the server's address. Confirm the actual published port in compose.yaml or with docker compose ps.
10. Kubernetes Deployment
The Kubernetes manifests are stored in the k8s/ directory. The application is deployed in the website namespace.
Prerequisites
- A working Kubernetes cluster.
- kubectl configured to access the intended cluster.
- A working cluster network plugin.
- Nginx Ingress Controller if using the Ingress resource.
- The frontend and backend images available in Docker Hub.
Create the namespace
kubectl create namespace website --dry-run=client -o yaml | kubectl apply -f -
Apply the manifests
kubectl apply -f k8s/ -n website
Set the application images
The backend and frontend Deployment container names used by the Jenkins pipeline are backend-container and frontend-container.
kubectl set image deployment/frontend-deployment \
  frontend-container=chaudharysachin/technova-frontend:v1 \
  -n website

kubectl set image deployment/backend-deployment \
  backend-container=chaudharysachin/technova-backend:v1 \
  -n website
Use image tags that actually exist in Docker Hub and match the tags built by the pipeline. If a new tag is introduced, update the build, push, and deployment references consistently.
Check Kubernetes resources
kubectl get pods -n website -o wide
kubectl get deployments -n website
kubectl get services -n website
kubectl get ingress -n website
kubectl get events -n website --sort-by=.metadata.creationTimestamp
Wait for rollout completion
Check each Deployment separately:
kubectl rollout status deployment/backend-deployment -n website --timeout=180s
kubectl rollout status deployment/frontend-deployment -n website --timeout=180s
kubectl rollout status deployment/redis -n website --timeout=180s
kubectl rollout status waits for a Deployment rollout. A fixed sleep can provide an initial delay, but it does not prove that an application is healthy.
Access through Ingress
The Ingress manifest uses the host technova.local. For local testing, configure name resolution so technova.local resolves to the Ingress Controller's reachable IP address. Then access the application using the host configured in the manifest.
11. Jenkins CI/CD Pipeline
The repository includes a Jenkinsfile that automates the application delivery workflow.
Pipeline stages
1. Code Checkout: Clones the main branch from GitHub.
2. Build: Builds frontend and backend Docker images.
3. Push to DockerHub: Authenticates using a Jenkins credential and pushes both images.
4. Deploy to Kubernetes: Applies the manifests and updates the frontend and backend Deployment images.
5. Verify Deployment: Waits for Deployments to roll out and checks Pods, Deployments, Services, and Ingress.
Docker Hub credential
Create a Jenkins credential with:
- Kind: Username with password
- ID: docker-hub-cred
- Username: Your Docker Hub username
- Password: A Docker Hub Personal Access Token with the permissions needed to push images
Do not put Docker Hub passwords or tokens directly in the Jenkinsfile or Git repository.
Jenkins agent requirements
The Jenkins execution node needs:
- Docker CLI and access to the Docker daemon.
- kubectl.
- Network access to GitHub, Docker Hub, and the Kubernetes API server.
- A kubeconfig or other approved Kubernetes authentication method.
- Permission to build/push images and deploy the required resources.
For the lab setup, the kubeconfig is configured at:
/var/lib/jenkins/.kube/config
The Jenkins process must be able to read this file. The kubeconfig must point to the intended Kubernetes API endpoint. Avoid using a cluster-admin kubeconfig permanently in production; use a dedicated ServiceAccount or other identity with least-privilege RBAC permissions.
Pipeline deployment verification
The verification stage checks each Deployment individually, for example:
kubectl rollout status deployment/backend-deployment -n website --timeout=180s
kubectl rollout status deployment/frontend-deployment -n website --timeout=180s
kubectl rollout status deployment/redis -n website --timeout=180s
If a Deployment does not become Ready before its timeout, the pipeline should fail so the issue can be investigated.
12. Health Checks and Troubleshooting
A running Pod is not necessarily a healthy application. Check readiness, logs, probes, and Kubernetes events.
Inspect Pods and events
kubectl get pods -n website -o wide
kubectl describe pod POD_NAME -n website
kubectl get events -n website --sort-by=.metadata.creationTimestamp
Inspect application logs
kubectl logs deployment/backend-deployment -n website
kubectl logs deployment/frontend-deployment -n website
kubectl logs deployment/redis -n website
For a restarted container, inspect its previous logs:
kubectl logs POD_NAME -n website --previous
Backend CrashLoopBackOff
Check the backend logs first:
kubectl logs POD_NAME -n website --previous
Verify:
- The image contains the latest app.py.
- REDIS_HOST is set to redis.
- REDIS_PORT_NUMBER is set to 6379.
- The application listens on 0.0.0.0:5000.
- The health endpoint responds on /health.
If source code changes but the same image tag is reused, ensure the image is rebuilt and pushed. With imagePullPolicy: IfNotPresent, a node can reuse a locally cached image. Use a new version tag for reliable rollouts, or deliberately configure imagePullPolicy: Always.
Frontend Pods remain Pending
Inspect the Pod's Events section:
kubectl describe pod POD_NAME -n website
Look for scheduling errors such as insufficient CPU or memory, node taints, affinity constraints, or volume-binding problems.
InvalidImageName or ImagePullBackOff
Check the image reference in the Deployment:
kubectl get deployment DEPLOYMENT_NAME -n website \
  -o jsonpath='{.spec.template.spec.containers[*].image}'
Verify that the image name and tag are valid and that the image exists in the registry.
Redis connection failure
Verify the Redis Pod and Service:
kubectl get pods,svc -n website
kubectl describe svc redis -n website
Confirm that the backend uses the Redis Service DNS name and the correct port.
13. Security and Optimization
- Run application containers as non-root users where possible.
- Do not store credentials in source code or container images.
- Use Jenkins credentials for registry authentication.
- Restrict Kubernetes permissions using least-privilege RBAC.
- Keep Redis on a private application network.
- Use explicit image tags rather than relying on latest.
- Use appropriate CPU and memory requests and limits.
- Configure readiness and liveness probes based on application behavior.
- Review exposed ports, container capabilities, and filesystem permissions.
- Use .dockerignore to exclude Git history, secrets, temporary files, and unnecessary content.
14. Recovery and Rollback
If a deployment fails:
1. Inspect Pod status, events, and application logs.
2. Identify whether the issue is in the image, application, configuration, networking, or cluster resources.
3. Restore a known-good image tag or configuration.
4. Wait for the affected Deployment rollout.
5. Verify application health and service access.
For Kubernetes, a previous Deployment revision can be inspected and restored with:
kubectl rollout history deployment/backend-deployment -n website
kubectl rollout undo deployment/backend-deployment -n website
Avoid deleting the namespace or persistent volumes as an automatic failure action. Namespace deletion removes all namespaced resources and can destroy application state.
15. Project Outcome
This project provides practical experience with:
- Docker image creation and container execution.
- Docker Compose multi-service deployments.
- Nginx reverse proxy configuration.
- Private service networking.
- Redis caching and TTL expiration.
- Python API development and health endpoints.
- Kubernetes Deployments, Services, and Ingress.
- Container resource requests and limits.
- Readiness and liveness probes.
- Jenkins declarative pipelines.
- Docker Hub authentication and image publishing.
- Kubernetes deployment automation and rollout verification.
- Troubleshooting image, application, and cluster failures.
16. Future Improvements
- Use unique image tags such as the Jenkins build number or Git commit SHA.
- Add automated frontend and backend tests before building images.
- Add image vulnerability scanning.
- Add Prometheus and Grafana monitoring.
- Use a dedicated Jenkins Kubernetes ServiceAccount with restricted RBAC.
- Add Kubernetes resource manifests validation to the pipeline.
- Add a controlled rollback stage.
- Add TLS for external application access.
- Introduce secret management for application credentials.