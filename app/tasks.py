import time
from app.celery_app import celery

@celery.task
def send_welcome_message(patient_name):

    print(f"Preparing welcome message for {patient_name}...")

    time.sleep(5)

    print(f"Welcome message sent to {patient_name}")

    return True