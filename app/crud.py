from sqlalchemy.orm import Session

from app.models import Patient
from app.schemas import PatientCreate

from app.services.patient_service import (
    calculate_bmi,
    get_verdict
)

def create_patient(db: Session, patient: PatientCreate):
    bmi = calculate_bmi(patient.weight, patient.height)
    verdict = get_verdict(bmi)

    db_patient = Patient(
        id= patient.id,
        name= patient.name,
        city= patient.city,
        age= patient.age,
        gender= patient.gender,
        height=patient.height,
        weight= patient.weight,
        bmi= bmi,
        verdict= verdict,
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient

def get_all_patients(db: Session):
    return db.query(Patient).all()

def get_patient_by_id(db: Session, patient_id: str):
    return(
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

def update_patient(db: Session, patient_id: str, patient_update):

    patient = (
        db.quer(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )
    if patient is None:
        return None
    
    update_data = patient_update.model_dump(exclude_unset = True)

    for key, value in update_data.items():
        setattr(patient, key, value)

    #Calculate bmi and verdict again
    patient.bmi = calculate_bmi(patient.weight, patient.height)
    patient.verdict = get_verdict(patient.bmi)

    db.commit()
    db.refresh(patient)

    return patient    


def delete_patient(db: Session, patient_id: str):

    patient =(
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        return False
    
    db.delete(patient)

    db.commit()

    return True


