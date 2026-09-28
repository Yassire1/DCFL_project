# Docker Compose + GPU Setup for Ubuntu Server

> Complete guide to run the DCFL Wind Turbine FL project on an Ubuntu Server with GPU support.

## Prerequisites

| Requirement | Why | How to check |
|------------|-----|-------------|
| Ubuntu Server 22.04 or 24.04 LTS | Docker official support | `lsb_release -a` |
| NVIDIA GPU driver installed | GPU access in containers | `nvidia-smi` (must show your GPU) |
| SSH access to the server | Remote terminal | `ssh your_user@SERVER_IP` |
| Git installed | Clone the project | `git --version` |

> **IMPORTANT:** If `nvidia-smi` does not show your GPU, install the NVIDIA driver first
> before proceeding. On Ubuntu Server, the easiest way is:
> ```bash
> sudo apt update
> sudo apt install -y ubuntu-drivers-common
> sudo ubuntu-drivers autoinstall
> sudo reboot
> ```
> After reboot, run `nvidia-smi` again to verify.

---

## Step 1: Install Docker Engine

This is the official method from [Docker's documentation](https://docs.docker.com/engine/install/ubuntu/).

### 1.1 Remove old versions

```bash
sudo apt remove -y docker.io docker-compose docker-compose-v2 docker-doc \
  docker-buildx podman-docker containerd runc 2>/dev/null
```

> Ignore errors if some packages are not installed.

### 1.2 Set up Docker's apt repository

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Add Docker's GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

### 1.3 Install Docker packages

```bash
sudo apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

### 1.4 Start and enable Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### 1.5 Allow non-root Docker access (optional but recommended)

```bash
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### 1.6 Verify Docker installation

```bash
docker --version
# Should show: Docker version 27.x.x or later

docker compose version
# Should show: Docker Compose version v2.x.x
```

---

## Step 2: Install NVIDIA Container Toolkit

This enables Docker containers to access your GPU. Official docs: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

### 2.1 Add NVIDIA repository

```bash
# Add GPG key
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# Add repository
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
```

### 2.2 Install the toolkit

```bash
sudo apt install -y nvidia-container-toolkit
```

### 2.3 Configure Docker to use NVIDIA runtime

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

This modifies `/etc/docker/daemon.json` to add the NVIDIA runtime.

### 2.4 Restart Docker

```bash
sudo systemctl restart docker
```

### 2.5 Verify GPU access in Docker

```bash
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

You should see your GPU listed in the output. If this works, GPU access in containers is working.

---

## Step 3: Clone and Run the FL Project

### 3.1 Clone the repository

```bash
git clone <your-repo-url>
cd DCFL_project/flower-WindPrediction
```

### 3.2 Verify data files exist

```bash
ls Data/
# Should show:
# turbine_T01_dataset.csv
# turbine_T06_dataset.csv
# turbine_T07_dataset.csv
# turbine_T11_dataset.csv
```

### 3.3 (Optional) Update Flower version

Your `compose.yml` uses `FLWR_VERSION:-1.18.0`. The current stable release is `1.38.0`.

```bash
sed -i 's/FLWR_VERSION:-1.18.0/FLWR_VERSION:-1.38.0/g' compose.yml
```

### 3.4 Build and start the Flower infrastructure

```bash
docker compose up --build -d
```

This starts:
- **SuperLink** (coordination server) on port 9093
- **ServerApp** (aggregation logic)
- **3 SuperNodes** (one per turbine client: T01, T06, T07)
- **3 ClientApps** (one per turbine)

### 3.5 Verify services are running

```bash
docker compose ps
```

All services should show `Up` status.

### 3.6 Start the federated training

```bash
flwr run . local-deployment --stream
```

> **Note:** You need `flwr` CLI installed on the host:
> ```bash
> pip install -U "flwr"
> ```

### 3.7 Monitor logs (in a separate terminal)

```bash
docker compose logs -f
```

### 3.8 Stop everything when done

```bash
docker compose down
```

---

## Quick Reference: Common Commands

| Task | Command |
|------|---------|
| Start infrastructure | `docker compose up --build -d` |
| Stop everything | `docker compose down` |
| Check status | `docker compose ps` |
| View logs | `docker compose logs -f` |
| View specific service logs | `docker compose logs -f serverapp` |
| Rebuild after code changes | `docker compose up --build -d` |
| Start FL training | `flwr run . local-deployment --stream` |
| Check GPU usage | `nvidia-smi` |
| Interactive shell in container | `docker compose run --rm clientapp-1 /bin/bash` |

---

## Troubleshooting

### `nvidia-smi` works on host but not in container

```bash
# Re-configure Docker runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### `docker compose up` fails with "port already in use"

```bash
# Find what's using the port
sudo lsof -i :9093

# Either stop the conflicting service or change the port in compose.yml
```

### Container build fails with "permission denied"

```bash
# Make sure your user is in the docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### `flwr run` can't connect to SuperLink

```bash
# Check if SuperLink is running
docker compose ps

# Check Flower config
flwr config list

# If needed, add the connection manually:
# Edit ~/.flwr/config.toml and add:
# [superlink.local-deployment]
# address = "127.0.0.1:8000"
# insecure = true
```

### Containers can't see GPU memory

```bash
# Verify NVIDIA runtime is configured
cat /etc/docker/daemon.json
# Should contain: "nvidia" as default runtime

# If not, re-run:
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

---

## Architecture Overview

```
Your PC (SSH) ────────────────────────── Ubuntu Server
                                          │
                                          ├── Docker
                                          │   ├── SuperLink (coordination)
                                          │   ├── ServerApp (aggregation)
                                          │   ├── SuperNode-1 → ClientApp-1 (T01)
                                          │   ├── SuperNode-2 → ClientApp-2 (T06)
                                          │   └── SuperNode-3 → ClientApp-3 (T07)
                                          │
                                          └── NVIDIA GPU (RTX 4080)
                                              └── T11 test data (server-side eval)
```

All 3 clients + server evaluation run on the same GPU via Flower's Docker deployment.
