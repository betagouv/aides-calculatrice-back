ARG PYTHON_IMAGE=python:3.11-slim

FROM $PYTHON_IMAGE AS base

# All deps stage
FROM base AS deps
WORKDIR /app

# Install build dependencies for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and project dependencies
RUN pip install poetry==1.8.3
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not create virtual environment and install globally
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only=main

# Production stage
FROM base AS production
ENV PORT=5000
WORKDIR /app

# Create non-root user
RUN groupadd -g 1001 python && \
    useradd -r -u 1001 -g python openfisca && \
    chown -R openfisca:python /app

# Copy the installed packages from deps stage
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

USER openfisca
EXPOSE $PORT

CMD ["openfisca", "serve", "--country-package", "openfisca_france", "--bind", "0.0.0.0:5000", "--timeout", "120"]
