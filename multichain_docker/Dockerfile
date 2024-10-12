# Base image
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    netcat \
    tar \
    python3 \
    build-essential

# Download and install Multichain
RUN curl -O https://www.multichain.com/download/multichain-2.3.2.tar.gz \
    && tar -xvzf multichain-2.3.2.tar.gz \
    && cd multichain-2.3.2 \
    && mv multichaind multichain-cli multichain-util /usr/local/bin/ \
    && rm -rf multichain-2.3.2*

# Expose Multichain's default ports
EXPOSE 8000 7447 2787
