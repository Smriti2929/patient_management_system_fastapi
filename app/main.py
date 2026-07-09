from fastapi import FastAPI
from app.api.patients import router as patient_router

app = FastAPI(
    title="Patient Management API",
    version="2.0"
)

app.include_router(patient_router)

@app.get("/")
def home():
    return {
        "message": "Patient Management API using FASTAPI + PostgreSQL"
    }
              