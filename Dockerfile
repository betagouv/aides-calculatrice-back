ARG PYTHON_IMAGE=python:3.11-slim

FROM $PYTHON_IMAGE AS base
RUN apt-get update && apt-get install -y --no-install-recommends \
    dumb-init \
    curl \
    && rm -rf /var/lib/apt/lists/*

# All deps stage
FROM base AS deps
WORKDIR /app
# Install build dependencies for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry temporarily to export requirements
RUN pip install poetry==1.8.3
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --only=main --without-hashes
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Build stage
FROM base AS build
WORKDIR /app
COPY --from=deps /app/venv /app/venv
COPY . .

# Production stage
FROM base AS production
ENV PORT=5000
WORKDIR /app

# Create non-root user
RUN groupadd -g 1001 python && \
    useradd -r -u 1001 -g python python

# Copy virtual environment and app code
COPY --from=build --chown=python:python /app/venv /app/venv
COPY --from=build --chown=python:python /app/aides_calculatrice_back /app/aides_calculatrice_back
COPY --from=build --chown=python:python /app/pyproject.toml ./

# Make sure we use venv
ENV PATH="/app/venv/bin:$PATH"

USER python
EXPOSE $PORT

CMD ["dumb-init", "openfisca", "serve", "--country-package", "openfisca_france", "--bind", "0.0.0.0:5000", "--timeout", "120"]
