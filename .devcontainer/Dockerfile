# MCP Service Development Container
# Author: Chandra Shettigar <chandra@devteds.com>

FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create non-root user (if not already created by base image)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Set up the user environment
USER $USERNAME

# Set environment variables
ENV PYTHONPATH=/workspace
ENV PATH=/home/$USERNAME/.local/bin:$PATH

WORKDIR /workspace

# Default command
CMD ["/bin/bash"] 