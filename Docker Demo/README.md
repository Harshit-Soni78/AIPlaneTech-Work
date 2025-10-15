# Docker Demo

A containerized Flask web application demonstrating Docker deployment best practices. This project showcases how to package a Python web application into a Docker container, manage dependencies, and deploy it consistently across different environments.

## 🚀 Features

- **Containerized Application**: Complete Docker setup for Flask app
- **Multi-stage Builds**: Optimized Docker image building
- **Dependency Management**: Isolated Python environment
- **Port Configuration**: Proper container networking
- **Production Ready**: Gunicorn WSGI server configuration
- **Development Support**: Debug mode and hot reloading
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Tech Stack

- **Application Framework**: Flask (Python web framework)
- **Container Runtime**: Docker
- **WSGI Server**: Gunicorn (production deployment)
- **Base Image**: Python slim image for smaller footprint
- **Web Server**: Built-in Flask development server

## 📋 Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose (optional, for orchestration)
- Git (for cloning repository)
- Web browser for testing

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Docker-Demo
   ```

2. **Verify Docker installation**:

```bash
docker --version
docker-compose --version
```

## 🎯 Usage

### Building the Docker Image

Build the Docker image:

```bash
docker build -t flask-docker-demo .
```

**Build options**:

- `-t flask-docker-demo`: Tag the image with a name
- `--no-cache`: Force rebuild without cache
- `-f Dockerfile`: Specify custom Dockerfile name

### Running the Container

Run the containerized application:

```bash
docker run -p 5000:5000 flask-docker-demo
```

**Run options**:

- `-p 5000:5000`: Map container port 5000 to host port 5000
- `-d`: Run in detached mode (background)
- `--name my-flask-app`: Assign container name
- `-e FLASK_ENV=development`: Set environment variables

### Accessing the Application

Open your browser and navigate to:

```
http://localhost:5000
```

## 📁 Project Structure

```
Docker Demo/
├── app.py                 # Flask application
├── Dockerfile            # Docker image configuration
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
├── .gitignore           # Git ignore rules
├── static/              # Static assets (CSS, JS, images)
├── templates/           # Jinja2 templates
│   ├── home.html        # Home page template
│   └── about.html       # About page template
└── (other files)
```

## 🐳 Dockerfile Explained

### Base Image

```dockerfile
FROM python:3.11-slim
```

- Uses Python 3.11 slim image for smaller size
- Includes only essential Python runtime

### Working Directory

```dockerfile
WORKDIR /app
```

- Sets `/app` as the working directory inside container
- All subsequent commands run from this directory

### Dependencies

```dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```

- Copies requirements file first (for better caching)
- Installs dependencies without cache to reduce image size

### Application Code

```dockerfile
COPY . .
```

- Copies all application files to container
- Includes source code, templates, and static files

### Port Exposure

```dockerfile
EXPOSE 5000
```

- Documents that container listens on port 5000
- Doesn't actually publish the port (done at runtime)

### Startup Command

```dockerfile
CMD ["python", "app.py"]
```

- Defines the command to run when container starts
- Uses production server (no debug mode)

## 🌐 Flask Application

### Routes

```python
@app.route("/", methods=["GET", "POST"])
def home():
    # Handle GET and POST requests
    # Render home template with optional name parameter

@app.route("/about")
def about():
    # Render about page
```

### Template Rendering

- Uses Jinja2 templating engine
- Supports dynamic content injection
- Bootstrap for responsive design

## 🚀 Deployment Options

### Development Mode

```bash
# Run with debug mode and auto-reload
docker run -p 5000:5000 -e FLASK_ENV=development flask-docker-demo
```

### Production Mode

```bash
# Use Gunicorn for production
docker run -p 8000:8000 -e FLASK_ENV=production flask-docker-demo
```

### Docker Compose

```yaml
version: "3.8"
services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    volumes:
      - .:/app
```

## 🔍 Docker Commands Reference

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi flask-docker-demo

# View image layers
docker history flask-docker-demo
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# View container logs
docker logs <container_id>

# Execute commands in running container
docker exec -it <container_id> bash
```

### Debugging

```bash
# Check container resource usage
docker stats <container_id>

# Inspect container configuration
docker inspect <container_id>

# View container filesystem
docker exec -it <container_id> ls -la /app
```

## 📊 Optimization Techniques

### Multi-stage Builds

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Image Size Reduction

- Use slim base images
- Remove package cache after installation
- Use `.dockerignore` to exclude unnecessary files
- Multi-stage builds to separate build and runtime

### Performance Optimization

- **Layer Caching**: Order Dockerfile commands for optimal caching
- **Dependency Management**: Separate requirements installation
- **Volume Mounting**: Mount source code for development
- **Resource Limits**: Set memory and CPU limits

## 🔒 Security Best Practices

### Image Security

- Use official base images
- Scan images for vulnerabilities
- Run containers as non-root user
- Keep images updated

### Container Security

```dockerfile
# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
```

### Secret Management

- Don't bake secrets into images
- Use environment variables or secret mounts
- Rotate credentials regularly

## 🧪 Testing

### Manual Testing

1. **Build Image**: `docker build -t flask-docker-demo .`
2. **Run Container**: `docker run -p 5000:5000 flask-docker-demo`
3. **Test Endpoints**:
   - `http://localhost:5000` (GET/POST)
   - `http://localhost:5000/about` (GET)
4. **Check Logs**: `docker logs <container_id>`

### Automated Testing

```bash
# Run tests inside container
docker run --rm flask-docker-demo python -m pytest

# Run linting
docker run --rm flask-docker-demo flake8 app.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Find process using port
   lsof -i :5000
   # Kill process or use different port
   docker run -p 5001:5000 flask-docker-demo
   ```

2. **Container Won't Start**

   ```bash
   # Check logs
   docker logs <container_id>
   # Debug interactively
   docker run -it --entrypoint bash flask-docker-demo
   ```

3. **Module Not Found**

   - Ensure all dependencies in `requirements.txt`
   - Check Python path in container
   - Verify imports in application code

4. **Permission Denied**
   - Check file permissions in host directory
   - Ensure user has Docker permissions
   - Use `sudo` if necessary (not recommended)

### Debug Commands

```bash
# Enter running container
docker exec -it <container_id> bash

# Check Python installation
docker exec <container_id> python --version

# Test Flask app manually
docker exec <container_id> python -c "from app import app; print('App imported successfully')"
```

## 📈 Performance Monitoring

### Resource Usage

```bash
# Monitor container resources
docker stats <container_id>

# Check container logs
docker logs -f <container_id>
```

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build and Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t flask-app .
      - name: Test application
        run: docker run --rm flask-app python -c "from app import app; print('Tests passed')"
```

### Deployment Scripts

```bash
#!/bin/bash
# Deploy script
docker build -t flask-app:$TAG .
docker stop flask-app || true
docker rm flask-app || true
docker run -d --name flask-app -p 5000:5000 flask-app:$TAG
```

## 📚 Learning Resources

### Docker Documentation

- [Docker Official Docs](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose](https://docs.docker.com/compose/)

### Flask Deployment

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.0.x/deploying/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)

### Container Orchestration

- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Docker Swarm](https://docs.docker.com/engine/swarm/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes to application or Dockerfile
4. Test changes locally with Docker
5. Submit pull request with description

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:

- Check Docker documentation
- Review container logs for errors
- Test with minimal example first
- Create an issue for bugs or features

---

**Note**: This demo focuses on basic Docker containerization. For production deployments, consider orchestration tools like Kubernetes, proper logging, monitoring, and security hardening.
