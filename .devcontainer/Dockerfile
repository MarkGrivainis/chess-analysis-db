FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Copy uv and uvx binaries from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace