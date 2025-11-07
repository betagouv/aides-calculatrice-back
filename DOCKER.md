# Docker Setup

This project includes Docker configuration for easy deployment in external infrastructure.

## Building the Docker image

```bash
docker build -t aides-calculatrice-back .
```

## Running with Docker

```bash
docker run -p 5000:5000 aides-calculatrice-back
```

## Running with Docker Compose

```bash
docker-compose up
```

The API will be available at `http://localhost:5000`.

## Environment Variables

- `PORT`: The port on which the service runs (default: 5000)

## Health Check

The service includes a health check endpoint at `/spec` that returns the OpenFisca API specification.

## Multi-stage Build

The Dockerfile uses multi-stage builds to optimize the final image size:

1. **base**: Sets up Python environment and installs Poetry
2. **deps**: Installs Python dependencies
3. **build**: Copies application code
4. **production**: Final minimal image with only runtime dependencies

## Security

- Runs as non-root user (`python:python` with UID/GID 1001)
- Uses `dumb-init` as PID 1 for proper signal handling
- Minimal attack surface with slim base image
