import json
from app.database import SessionLocal
from app.models import Patient

db = SessionLocal()

with open("patients.json", "r") as f:
    data = json.load(f)

for patient_id, patient in data.items():
    existing = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if existing:
        continue

    db_patient = Patient(
        id = patient_id,
        name = patient["name"],
        city=patient["city"],
        age=patient["age"],
        gender=patient["gender"],
        height=patient["height"],
        weight=patient["weight"],
        bmi=patient["bmi"],
        verdict=patient["verdict"]
    )    

    db.add(db_patient)

db.commit()
db.close()

print("Patients imported successfully!")