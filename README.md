# TechNova Solutions — Dockerized Web Application

## Project Overview

TechNova Solutions is a company website deployed using Docker and Docker Compose. The project demonstrates containerization of a static frontend and a Python backend API, including reverse proxy configuration, persistent storage, health checks, container networking, and image publishing.

The objective is to create a portable and maintainable application that can be deployed consistently across Linux environments.

## Technology Stack

- Linux (Ubuntu / RHEL)
- Docker
- Docker Compose
- Nginx
- Python 3.12
- HTML5 and CSS3
- Docker Hub

## Architecture

The application consists of two containers:

1. **Frontend:** Nginx serves the website and forwards API requests to the backend.
2. **Backend:** A Python HTTP API provides service information, health status, and a persistent visit counter.

Both containers communicate over a private Docker network. Only the frontend port is published on the host.

```text
User Browser
     |
     | HTTP :8081
     v
Frontend Container (Nginx :80)
     |
     | /api/* requests
     v
Backend Container (Python :5000)
     |
     v
Named Docker Volume (/data)
```

## Project Structure

```text
company-website/
├── index.html
├── style.css
├── nginx.conf
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── README.md
└── backend/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

## Application Features

- Company introduction, services, and contact sections.
- Four service categories:
  - Cloud Computing
  - DevOps Automation
  - Linux Administration
  - Monitoring and Observability
- Python API for retrieving service information.
- Health endpoint for backend monitoring.
- Visit counter stored in persistent data.
- Nginx reverse proxy for API requests.
- Separate frontend and backend containers.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | Returns backend health status |
| `/api/services` | Returns company information and services |
| `/api/visits` | Increments and returns the visit counter |

The API is intended to be accessed through the frontend's Nginx reverse proxy.

## Docker Configuration

### Frontend

The frontend uses Nginx Alpine to serve the HTML and CSS files. The Nginx configuration forwards API requests to the backend Compose service.

### Backend

The backend uses Python 3.12 Slim and runs the application as a non-root user. Its data directory is mounted from a named Docker volume.

### Networking

Docker Compose creates a private application network for communication between the frontend and backend. The backend is not published directly on a host port.

### Persistent Storage

A named Docker volume is mounted at `/data` inside the backend container.

The volume preserves the visit-counter data when the backend container is recreated, provided the volume itself is retained.

## Deployment

### Prerequisites

- A Linux server with Docker installed.
- Docker Compose support.
- Git, if cloning the project from GitHub.
- Network access to the server's published frontend port.

### Build and Start

From the project root, build the images and start the services using Docker Compose.

```bash
docker compose build
docker compose up -d
```

### Verify the Containers

```bash
docker compose ps
docker compose logs
```

Confirm that both services are running and that the configured health checks report healthy status.

### Access the Website

Open the following URL in a browser, replacing the address with the server's actual IP:

`http://YOUR_SERVER_IP:8081`

## Validation and Testing

The following checks should be completed before considering the deployment successful:

- Confirm that the website loads in a browser.
- Confirm that all four services are displayed.
- Verify that `/api/services` returns JSON through the frontend URL.
- Verify that `/health` reports the expected backend status.
- Confirm that the backend port is not published directly on the host.
- Verify that the visit counter persists after container recreation.
- Confirm that both containers recover correctly after a controlled restart.
- Inspect container logs for application or proxy errors.

## Troubleshooting

### Website Is Not Accessible

Check the frontend container status, published port mapping, Nginx configuration, and host firewall.

### API Returns 404

Check whether Nginx has a matching `/api/` location and whether the proxy configuration is present in the running frontend container.

### API Returns 502

Check the backend container status, Compose network membership, service name, internal port, and Nginx error logs.

### Backend Is Unhealthy

Inspect the backend logs and verify that the health endpoint responds successfully from inside the container.

### Visit Counter Resets

Verify that the named volume is mounted at the application's configured data directory and that the backend has write permission. Confirm that the volume was not deleted.

## Security and Optimization

- Run the backend as a non-root user.
- Avoid privileged containers unless there is a justified requirement.
- Do not hard-code credentials into images or source code.
- Use `.dockerignore` to exclude unnecessary files from the build context.
- Use explicit image version tags.
- Review exposed ports and container capabilities.
- Use suitable health checks and restart policies.
- Inspect image sizes and remove unnecessary files and layers.

## Docker Hub Publishing

Publish versioned frontend and backend images to Docker Hub using the appropriate repository names.

Example naming convention:

- chaudharysachin/technova-website:v2.0`
- chaudharysachin/technova-api:v2.0`

After publishing, verify that the images can be pulled and deployed on a separate test environment.

## Recovery and Rollback

If a deployment fails:

1. Inspect container status and logs.
2. Identify whether the issue is related to the image, configuration, networking, or application.
3. Restore the last known-good image version and configuration.
4. Recreate the affected service.
5. Verify frontend access, API responses, and health checks.
6. Confirm that persistent data remains intact.

Avoid removing named volumes during recovery unless their deletion is intentional.

## Project Outcome

This project demonstrates practical skills in Docker image creation, container management, Docker Compose, Nginx reverse proxy configuration, private networking, persistent storage, health checks, basic container security, troubleshooting, and image publishing.

## Future Improvements

- Integrate the application with a Jenkins CI/CD pipeline.
- Add automated application tests.
- Publish images automatically after successful builds.
- Introduce image vulnerability scanning.
- Add Prometheus and Grafana monitoring.
- Deploy the application to Kubernetes.
