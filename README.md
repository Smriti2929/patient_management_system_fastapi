# 🏥 FastAPI Patient Management System

A production-inspired RESTful Patient Management API built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis**, **Celery**, **Alembic**, and **Docker**.

The project demonstrates modern backend development practices including layered architecture, ORM-based database interactions, asynchronous background processing, caching, database migrations, and containerized deployment.

---

## 🚀 Features

### Patient Management

- Create Patient
- Retrieve All Patients
- Retrieve Patient by ID
- Update Patient Information
- Delete Patient

### Automatic Health Analytics

- Automatic BMI Calculation
- Automatic Health Verdict Generation

### Backend Features

- FastAPI REST API
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Database Migrations
- Redis Caching
- Celery Background Tasks
- Docker & Docker Compose
- Layered Project Architecture
- Environment Variable Configuration

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database Migration | Alembic |
| Cache | Redis |
| Background Jobs | Celery |
| API Server | Uvicorn |
| Containerization | Docker, Docker Compose |

---

# 📁 Project Structure

```text
fastapi-patient-api/

│
├── app/
│   ├── api/
│   │   └── patients.py
│   │
│   ├── services/
│   │   └── bmi.py
│   │
│   ├── __init__.py
│   ├── celery_app.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── redis_client.py
│   ├── schemas.py
│   └── tasks.py
│
├── alembic/
│
├── screenshots/
│
├── scripts/
│   └── seed_db.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# 🏗 Architecture

```text
                     Client

                        │
                        ▼

                 FastAPI REST API

                /                 \
               ▼                   ▼

      SQLAlchemy ORM         Redis Cache

               │                   │

               ▼                   ▼

        PostgreSQL DB       Celery Worker

               │                   │

               └──────► Background Tasks
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients` | Retrieve all patients |
| GET | `/patients/{id}` | Retrieve patient by ID |
| POST | `/patients` | Create a new patient |
| PUT | `/patients/{id}` | Update patient details |
| DELETE | `/patients/{id}` | Delete patient |

---

# ⚙ Local Setup

## Clone Repository

```bash
git clone https://github.com/Smriti2929/fastapi-patient-api.git

cd fastapi-patient-api
```

---

## Create Virtual Environment

```bash
python -m venv myenv
```

Windows

```bash
myenv\Scripts\activate
```

Linux / Mac

```bash
source myenv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/patient_db

REDIS_URL=redis://localhost:6379/0
```

---

## Apply Database Migrations

```bash
alembic upgrade head
```

---

## Start Redis

```bash
docker run -d -p 6379:6379 redis:7
```

---

## Start Celery Worker

```bash
celery -A app.celery_app.celery worker --loglevel=info
```

---

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 🐳 Running with Docker

```bash
docker compose up --build
```

The application, PostgreSQL, Redis, and Celery Worker will start automatically.

---

# ⚡ Background Tasks

Whenever a patient is created:

- Patient data is stored in PostgreSQL.
- A background task is queued in Redis.
- Celery Worker processes the task asynchronously.
- The API responds immediately without waiting for task completion.

---

# 📸 Screenshots

### Swagger Documentation
![Swagger UI](screenshots/swagger-ui.png)

### Create Patient
![Create Patient](screenshots/create-patient.png)

![Created Patient Successfully](screenshots/create-patient-success.png)

### Retrieve Patient
![Retrieve Patient](screenshots/view-patient.png)

![Retrieved Patient](screenshots/view-patient-success.png)

### Update Patient Information
![Update Patient](screenshots/update-patient.png)

![Updated Patient](screenshots/update-patient-success.png)

![Before Updating Patient](screenshots/update-patient-before.png)

![After Updating Patient](screenshots/update-patient-after.png)

### Sort Patients by BMI
![Sort Patients](screenshots/sort-patients.png)

![Sorted Patients](screenshots/sort-patients-success.png)

---

# 🔮 Future Improvements

- JWT Authentication
- Role-Based Access Control
- Pytest Unit Tests
- GitHub Actions CI/CD
- Kubernetes Deployment
- RabbitMQ Message Broker
- Neo4j Integration

---


