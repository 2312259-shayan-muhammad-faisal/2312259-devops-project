# 2312259 — DevOps Fundamentals Final Project

**Student:** Shayan Muhammad Faisal  
**Registration Number:** 2312259  
**Project:** Containerised Microservice with Automated CI/CD and Cloud Deployment

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                                │
│  Push to any branch  ──►  CI Pipeline (lint + test)         │
│  Push to main        ──►  CD Pipeline (deploy to EC2)       │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼ SSH
┌─────────────────────────────────────────────────────────────┐
│                     AWS EC2 (t2.micro)                       │
│                                                             │
│  ┌──────────────────┐      ┌──────────────────────────┐    │
│  │  FastAPI + Uvicorn│◄────►│    PostgreSQL 15          │    │
│  │  Port: 8000       │      │    Port: 5432             │    │
│  └──────────────────┘      │    Volume: postgres_data   │    │
│                             └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

| Component    | Technology              | Description                            |
|--------------|-------------------------|----------------------------------------|
| Web Service  | FastAPI + Uvicorn       | REST API on port 8000                  |
| Database     | PostgreSQL 15           | Persistent DB with named Docker volume |
| CI Pipeline  | GitHub Actions          | flake8 lint + pytest on every push/PR  |
| CD Pipeline  | GitHub Actions + SSH    | Auto-deploy to EC2 on push to main     |
| Cloud Server | AWS EC2 t2.micro        | Ubuntu 22.04 running Docker + Compose  |

---

## API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/health`          | Health check with DB status          |
| POST   | `/students`        | Create a new student record          |
| GET    | `/students`        | List all students                    |
| GET    | `/students/{reg_no}` | Get student by registration number |

---

## Local Setup Instructions

### Prerequisites
- Docker Desktop installed
- Git installed

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShayanMuhammadFaisal/2312259-devops-project.git
   cd 2312259-devops-project
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred values
   ```

3. **Start the application**
   ```bash
   docker compose up --build
   ```

4. **Test the endpoints**
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Create a student
   curl -X POST http://localhost:8000/students \
     -H "Content-Type: application/json" \
     -d '{"reg_no": "2312259", "name": "Shayan Muhammad Faisal", "email": "shayan@example.com"}'

   # List all students
   curl http://localhost:8000/students

   # Get by reg_no
   curl http://localhost:8000/students/2312259
   ```

5. **Stop the application**
   ```bash
   docker compose down
   ```

---

## Running Tests Locally

```bash
pip install -r requirements.txt
pytest app/tests/ -v
```

---

## EC2 Setup Instructions (One-Time)

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Update and install Docker
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu
newgrp docker

# Clone the project
git clone https://github.com/ShayanMuhammadFaisal/2312259-devops-project.git
cd 2312259-devops-project
```

---

## GitHub Secrets Required (for CD pipeline)

Add these in: Repository → Settings → Secrets and variables → Actions

| Secret Name       | Value                        |
|-------------------|------------------------------|
| `EC2_HOST`        | Your EC2 public IP address   |
| `EC2_USER`        | `ubuntu`                     |
| `EC2_SSH_KEY`     | Contents of your `.pem` file |
| `POSTGRES_USER`   | `postgres`                   |
| `POSTGRES_PASSWORD` | Your secure DB password    |
| `POSTGRES_DB`     | `devops_db`                  |

---

## Project Structure

```
2312259-devops-project/
├── app/
│   ├── main.py               ← FastAPI routes
│   ├── database.py           ← SQLAlchemy DB setup
│   ├── models.py             ← Student data model
│   └── tests/
│       ├── conftest.py       ← pytest fixtures and test DB
│       ├── test_health.py    ← Tests for /health
│       └── test_students.py  ← Tests for POST/GET /students
├── Dockerfile
├── docker-compose.yml        ← Local development
├── docker-compose.prod.yml   ← Production (EC2)
├── requirements.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── .github/
│   └── workflows/
│       ├── ci.yml            ← Lint + test
│       └── cd.yml            ← Deploy to EC2
└── README.md
```

## Docker Setup
Built with Docker + Docker Compose for containerised deployment

## CI/CD Pipeline
GitHub Actions runs flake8 and pytest on every push.
