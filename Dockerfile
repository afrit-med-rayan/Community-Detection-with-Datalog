# Use Ubuntu as the base image for easier Souffle installation
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Soufflé via Official PPA
RUN wget -q https://souffle-lang.github.io/ppa/souffle-key.public -O /usr/share/keyrings/souffle-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | tee /etc/apt/sources.list.d/souffle.list \
    && apt-get update \
    && apt-get install -y souffle

# 3. Set Working Directory
WORKDIR /app

# 4. Copy Project Files
COPY requirements.txt .
COPY src/ /app/src/

# 5. Install Python Dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 6. Expose Web Port
EXPOSE 5000

# 7. Start Web Server
CMD ["python3", "src/app.py"]
