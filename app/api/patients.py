from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PatientCreate, PatientResponse, PatientUpdate
from app.crud import create_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient
from app.models import Patient

import json
from app.redis_client import redis_client

from app.tasks import send_welcome_message

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/", response_model=PatientResponse, status_code=201)
def create_new_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    
    #check if patient exists already
    existing_patient = db.query(Patient).filter(
        Patient.id == patient.id
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )
    created_patient= create_patient(db, patient)
    send_welcome_message.delay(created_patient.name)
    return created_patient

@router.get("/", response_model=list[PatientResponse])
def read_patients(db: Session = Depends(get_db)):
    return get_all_patients(db)

@router.get("/{patient_id}", response_model=PatientResponse)
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    
    #Check Redis first
    cached_patient = redis_client.get(patient_id)
    
    if cached_patient:
        print("Returned from Redis")
        return json.loads(cached_patient)
    
    #if not found in Redis, fetch from PostgreSQL
    patient = get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    #Store in Redis for 60 seconds
    patient_data = {
        "id": patient.id,
        "name": patient.name,
        "city": patient.city,
        "age": patient.age,
        "gender": patient.gender,
        "height": patient.height,
        "weight": patient.weight,
        "bmi": patient.bmi,
        "verdict": patient.verdict
    }

    redis_client.setex(
        patient_id,
        60,
        json.dumps(patient_data)
    )

    print ("Fetched from PostgreSQL")

    return patient

@router.put("/{patient_id}", response_model= PatientResponse)
def update_existing_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = update_patient(
        db,
        patient_id,
        patient_update
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    redis_client.delete(patient_id)
    return patient


@router.delete("/{patient_id}")
def delete_existing_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    
    deleted = delete_patient(
        db,
        patient_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    redis_client.delete(patient_id)
    
    return {
        "message": "Patient deleted successfully"
    }
