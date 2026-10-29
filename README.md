# TechNova Solutions — Dockerized Web Application with Redis Caching

## 1. Project Overview

TechNova Solutions is a containerized web application built to practise Docker and Docker Compose from application deployment through production-oriented container management.

The project includes a static website served by Nginx, a Python backend API, and Redis for caching API responses. Docker Compose manages the services, networking, and persistent storage.

The application demonstrates containerization, reverse proxy configuration, private networking, persistent volumes, health checks, cache expiration, troubleshooting, and container security.

## 2. Technology Stack

- **Operating System:** Linux (Ubuntu / RHEL)
- **Container Runtime:** Docker
- **Container Orchestration:** Docker Compose
- **Frontend Web Server:** Nginx
- **Backend:** Python 3.12
- **Cache:** Redis
- **Frontend:** HTML5 and CSS3
- **Image Registry:** Docker Hub
- **Version Control:** Git and GitHub

## 3. Architecture

The application consists of three services.

1. **Frontend:** Nginx serves the static website and forwards API requests to the Python backend.
2. **Backend:** A Python HTTP API provides service information, health status, and visit-counter functionality.
3. **Redis:** Stores cached service responses with a 60-second expiration period.

The services communicate over a private Docker network. Only the frontend is published to the host.

```text
                 User Browser
                      |
                      | HTTP :8081
                      v
              +------------------+
              | Nginx Frontend   |
              | Container :80    |
              +------------------+
                      |
                      | /api/*
                      v
              +------------------+
              | Python Backend   |
              | Container :5000  |
              +------------------+
                      |
                      | Redis protocol
                      v
              +------------------+
              | Redis Cache      |
              | Container :6379  |
              +------------------+
```

### Network Design

- The frontend is accessible through host port `8081`.
- The backend listens on container port `5000`.
- Redis listens on container port `6379`.
- The backend and Redis communicate over the private Compose network.
- Backend and Redis ports should not be published directly on the host.

## 4. Project Structure

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

## 5. Application Features

- Company introduction and contact information.
- Four service categories:
  - Cloud Computing
  - DevOps Automation
  - Linux Administration
  - Monitoring and Observability
- Python API for service information.
- Nginx reverse proxy for API requests.
- Redis caching with a 60-second TTL.
- Backend health endpoint.
- Persistent visit-counter data using a named Docker volume.
- Separate frontend, backend, and Redis containers.
- Versioned application images.

## 6. API Endpoints

| Endpoint        | Purpose                                           |
| --------------- | ------------------------------------------------- |
| `/`             | Serves the website                                |
| `/api/services` | Returns company information and the four services |
| `/api/visits`   | Increments and returns the visit counter          |
| `/health`       | Checks backend health                             |

The API endpoints are intended to be accessed through the frontend's Nginx reverse proxy. The backend's internal port should not be exposed directly on the host.

## 7. Redis Caching

Redis is used to reduce repeated processing of the service-information API.

The backend stores the service response under the key `technova:services` with a TTL of 60 seconds.

### Cache Behavior

- **MISS:** The requested response is not in Redis, so the backend generates it and stores it in the cache.
- **HIT:** A valid cached response is returned.
- **Expiration:** After the TTL expires, the next request regenerates the response and stores it again.

### Cache Validation

The expected sequence is:

1. Clear the service cache entry.
2. Request `/api/services` and verify `MISS`.
3. Request it again and verify `HIT`.
4. Wait more than 60 seconds without refreshing the cache entry.
5. Request the API again and verify `MISS`.

Example response:

```json
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
```

The `cache` field is included for demonstration and validation.

## 8. Docker Configuration

### Frontend

The frontend image uses Nginx Alpine to serve the HTML and CSS files. The Nginx configuration forwards requests matching `/api/` to the backend service using the Compose service name.

### Backend

The backend image uses Python 3.12 Slim. It uses environment variables for its listening port, data directory, and Redis connection settings.

The backend should run as a non-root user and use a named volume for persistent visit-counter data.

### Redis

Redis stores cached API responses. The cache entry expires automatically after 60 seconds.

Redis cache persistence is separate from application-data persistence. The service cache can be regenerated after a Redis restart, while the visit counter should remain in its own named volume.

## 9. Deployment

### Prerequisites

- Linux server with Docker installed.
- Docker Compose support.
- Git, if cloning the project from GitHub.
- Network access to the frontend's published port.

### Build and Start

From the project root:

```bash
docker compose build
docker compose up -d
```

### Check Container Status

```bash
docker compose ps
```

### Inspect Logs

```bash
docker compose logs
```

For individual services, inspect the frontend, backend, or Redis logs separately.

### Access the Website

Open the following URL in a browser:

`http://YOUR_SERVER_IP:8081`

Replace `YOUR_SERVER_IP` with the actual address of the Linux server.

## 10. Health Checks

Health checks should verify actual service functionality.

- **Frontend:** Verify that Nginx can serve the website.
- **Backend:** Verify that the Python `/health` endpoint responds successfully.
- **Redis:** Verify that Redis responds to a health probe.

A running container is not necessarily a healthy container. Validate the configured health status and inspect service logs when a check fails.

## 11. Persistent Storage

The backend uses a named Docker volume mounted at `/data` for the visit counter.

The volume should preserve data when the backend container is recreated, provided the volume itself is retained and the application continues to use the same mount.

Validation procedure:

1. Make several requests to `/api/visits`.
2. Record the returned counter value.
3. Recreate the backend container without deleting the named volume.
4. Request `/api/visits` again.
5. Confirm that the counter continues from its previous value.

Redis cache entries are separate from the persistent visit counter.

## 12. Validation and Testing

The following tests should be completed before considering the deployment successful:

- Verify that the website loads in a browser.
- Confirm that all four services are returned by the API.
- Confirm that `/api/services` works through the Nginx proxy.
- Verify the `MISS`, `HIT`, and expiration behavior.
- Confirm that Redis has no host-published port.
- Verify that frontend, backend, and Redis are on the intended network.
- Confirm that configured health checks report the correct state.
- Verify that visit-counter data survives container recreation.
- Test backend and Redis recovery after a controlled failure.
- Inspect container logs for application and proxy errors.

## 13. Troubleshooting

### Website Is Not Accessible

Check frontend container status, host port mapping, Nginx configuration, and the host firewall.

### API Returns 404

Check whether Nginx has a matching `/api/` location and whether the proxy configuration is loaded into the running container.

### API Returns 502

Check backend availability, Compose network membership, service-name resolution, internal port, and Nginx error logs.

### Backend Is Unhealthy

Inspect the backend logs and verify that the health endpoint responds successfully inside the container.

### Redis Connection Failure

Verify the Redis container status, network membership, service name, internal port, and backend environment variables.

### Cache Always Returns MISS

Check that the backend writes and reads the same Redis key, that the TTL is configured correctly, and that requests reach the same Redis instance.

### Visit Counter Resets

Verify the named-volume mount, the configured data directory, write permissions, and whether the volume was removed or replaced.

## 14. Security and Optimization

- Run the backend as a non-root user.
- Avoid privileged containers unless required.
- Do not hard-code credentials into application files or images.
- Exclude Git history, secrets, temporary files, and unnecessary content using `.dockerignore`.
- Use explicit image version tags.
- Review published ports and container capabilities.
- Keep Redis on the private application network.
- Use suitable health checks and restart policies.
- Inspect image sizes and remove unnecessary files and layers.

## 15. Docker Hub

Publish versioned frontend and backend images to Docker Hub.

Example image names:

- chaudharysachin`/technova-website:v3.0`
- `chaudharysachin/technova-api:v3.0`

Choose tags that match the versions you actually built.

Redis can use an appropriate upstream image or a deliberately maintained custom image if customization is required.

After publishing, pull the application images into a separate test environment and verify that the application can be deployed using Compose.

Do not commit Docker Hub credentials or access tokens to the repository.

## 16. Recovery and Rollback

If a deployment fails:

1. Inspect service status and logs.
2. Identify whether the issue is related to the image, configuration, networking, Redis, or application code.
3. Restore the last known-good image version and configuration.
4. Recreate the affected service.
5. Verify frontend access, API responses, cache behavior, and health checks.
6. Confirm that the visit counter remains intact.

Avoid deleting named volumes during recovery unless their removal is intentional.

Redis cache data can generally be regenerated by the application after a cache loss. The visit-counter volume must be retained if that data needs to survive recovery.

## 17. Project Outcome

This project demonstrates practical experience with:

- Docker images and containers.
- Docker Compose multi-service deployments.
- Nginx reverse proxy configuration.
- Private container networking.
- Named volumes and persistent application data.
- Redis caching and TTL expiration.
- Container health checks and recovery.
- Container security and image optimization.
- Docker Hub image publishing.
- Application troubleshooting and technical documentation.

## 18. Future Improvements

- Integrate the application with Jenkins CI/CD.
- Add automated application tests.
- Introduce image vulnerability scanning.
- Add Prometheus and Grafana monitoring.
- Use Redis authentication and a managed secret-handling approach where appropriate.
- Deploy the application to Kubernetes.
