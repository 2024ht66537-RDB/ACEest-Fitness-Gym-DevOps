# 🏋️ ACEest Fitness & Gym — DevOps CI/CD Project

![CI Pipeline](https://github.com/<YOUR_USERNAME>/ACEest-Fitness-Gym-DevOps/actions/workflows/main.yml/badge.svg)

A Flask-based fitness and gym management REST API with a fully automated
CI/CD pipeline using **GitHub Actions** and **Jenkins**, containerised
with **Docker**.

---

## 📁 Project Structure

```
ACEest-Fitness-Gym-DevOps/
├── app.py                        # Flask application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── Jenkinsfile                   # Jenkins pipeline definition
├── .gitignore
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD workflow
├── tests/
│   ├── __init__.py
│   └── test_app.py               # Pytest test suite (30+ tests)
└── README.md
```

---

## 🚀 Local Setup & Execution

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### 1 — Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/ACEest-Fitness-Gym-DevOps.git
cd ACEest-Fitness-Gym-DevOps
```

### 2 — Create a virtual environment & install dependencies

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3 — Run the Flask application locally

```bash
python app.py
```

The API will be available at **http://localhost:5000**

### 4 — Test the API manually (cURL examples)

```bash
# Home
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# List members
curl http://localhost:5000/members

# Add a member
curl -X POST http://localhost:5000/members \
     -H "Content-Type: application/json" \
     -d '{"name":"Ravi Kumar","age":28,"plan":"premium"}'

# List classes
curl http://localhost:5000/classes

# Enroll in a class (class id = 1)
curl -X POST http://localhost:5000/classes/1/enroll

# BMI calculator
curl -X POST http://localhost:5000/bmi \
     -H "Content-Type: application/json" \
     -d '{"weight":70,"height":1.75}'
```

---

## 🧪 Running Tests Manually

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## 🐳 Docker Usage

### Build the image

```bash
docker build -t aceest-fitness-gym:latest .
```

### Run the container

```bash
docker run -d -p 5000:5000 --name gym-app aceest-fitness-gym:latest
```

### Run tests inside the container

```bash
docker run --rm \
  --entrypoint pytest \
  aceest-fitness-gym:latest \
  tests/ -v --tb=short
```

### Stop and remove the container

```bash
docker stop gym-app && docker rm gym-app
```

---

## ⚙️ GitHub Actions — CI/CD Pipeline

The workflow file is located at `.github/workflows/main.yml`.

**Trigger:** Every `push` or `pull_request` to any branch.

### Pipeline Stages

| Stage | Description |
|---|---|
| **Checkout** | Fetches the latest code from GitHub |
| **Setup Python** | Installs Python 3.11 and caches pip packages |
| **Install Dependencies** | Installs packages from `requirements.txt` |
| **Lint (flake8)** | Checks `app.py` for syntax and style errors |
| **Unit Tests (Pytest)** | Runs 30+ tests against the Flask application |
| **Docker Build** | Builds the Docker image from the `Dockerfile` |
| **Docker Test** | Re-runs the Pytest suite *inside* the Docker container |

The `docker` job only runs after the `build` job succeeds (`needs: build`).

---

## 🔧 Jenkins — BUILD Phase

The `Jenkinsfile` at the project root defines a declarative pipeline.

### Jenkins Setup Steps

1. **Install Jenkins** (LTS) on your server or local machine.
2. **Install required plugins:**  
   - Git Plugin  
   - Pipeline Plugin  
   - JUnit Plugin  
   - Docker Pipeline Plugin
3. **Create a new Pipeline job:**
   - Jenkins Dashboard → **New Item** → **Pipeline**
   - Under *Pipeline*, select **Pipeline script from SCM**
   - SCM: **Git** → paste your GitHub repo URL
   - Script Path: `Jenkinsfile`
4. **Save & Build Now**

### Jenkins Pipeline Stages

| Stage | Description |
|---|---|
| **Checkout** | Pulls latest code from GitHub |
| **Setup Python** | Creates a `venv` and installs dependencies |
| **Lint** | Runs flake8 to catch syntax errors |
| **Unit Tests** | Runs Pytest and publishes JUnit XML results |
| **Docker Build** | Builds the Docker image |
| **Docker Test** | Runs Pytest inside the container as final validation |

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message & version |
| GET | `/health` | Health check |
| GET | `/members` | List all members |
| POST | `/members` | Add a new member |
| GET | `/members/<id>` | Get a specific member |
| GET | `/classes` | List all gym classes |
| POST | `/classes/<id>/enroll` | Enroll in a class |
| POST | `/bmi` | Calculate BMI & category |

---

## 📋 Evaluation Checklist

- [x] Flask application with modular endpoints
- [x] Git repository with meaningful commits
- [x] 30+ Pytest unit tests covering all endpoints
- [x] Optimised, secure Dockerfile (non-root user, slim base)
- [x] GitHub Actions pipeline (lint → test → docker build → docker test)
- [x] Jenkinsfile for BUILD phase integration
- [x] Professional README with full documentation

---

*Submitted for Introduction to DevOps — Assignment 1*
