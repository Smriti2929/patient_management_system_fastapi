from fastapi import FastAPI, Path,Query, HTTPException # HTTP Exception : custom exception class 
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal,Optional, Annotated #to add description in fields

app = FastAPI() #fastapi object creation

class Patient(BaseModel): #patient inherits base model

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='Residing ')]
    age: Annotated [int, Field(..., gt=0, lt=120, description= 'Age of the Patient')]
    gender: Annotated[Literal['female', 'male', 'others'], Field(..., description='Gender of the Patient')] #Literal ensures only the given values are allowed
    height: Annotated[float, Field(..., gt=0, description='Height of the Patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float: 
        bmi = round((self.weight)/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return ('Underweight')
        elif self.bmi < 25 :
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
class Patient_Update(BaseModel):
        name: Annotated[Optional [str], Field(default=None)]
        city: Annotated[Optional [str], Field(default=None)]
        age: Annotated [Optional [int], Field(default=None, gt=0)]
        gender: Annotated[Optional [Literal['female', 'male', 'others']], Field(default=None)] 
        height: Annotated[Optional [float], Field(default=None, gt=0)]
        weight: Annotated[Optional [float], Field(default=None, gt=0)]    
        
        


def load_data():
    with open("patients.json", 'r')as f:
        data = json.load(f)

    return data 

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)    

@app.get("/") # created route with decorator (home route) and route listens to this get request 
def hello(): #func for hello world msg 
    return {"message": "Patient Management System API"} #reurns a dict. 

@app.get("/about")
def about():
    return {"message" : "A fully-functional API to manage your patient records"}

@app.get('/view')
def view():
    data =load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description = 'ID of the patient in the DB', example = 'P001'  )):

    data = load_data() #load all patients

    #check a specific patient
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code= 404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'Sort on basis of height, weight, bmi'), order: str = Query('asc', description = 'Sort in asc or desc order')) :
    
    valid_fields = ['height', 'weight', 'bmi']   #set valid fields to sort

    #validate sort_by parameter
    if sort_by not in valid_fields :
        raise HTTPException(
            status_code=400,
            detail= f'Invalid field. Select from {valid_fields}'
        )
    
    #validate order parameter
    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code= 400,
            detail= 'Invalid order. Select between asc and desc'
        )
    
    #load data
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(),
        key = lambda x : x.get(sort_by,0),
        reverse= sort_order
    )

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # add new patient to the database
    # data -> dict
    # In (patient: Patient), patient-> pydantic obj 
    # convert patient (pydantic obj) -> dict
    data[patient.id] = patient.model_dump(exclude=['id']) #model_dump converts obj into dict

    #save into json file 
    # (currently a dict so create utility save func to save into json format)
    save_data(data)

    return JSONResponse (status_code=201, content={'message': 'Patient Created Successfully!'})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: Patient_Update):
#patient_id -> path parameter se mil jaegi info
# patient_update -> variable that stores pydantic obj 
#Patient_update -> pydantic obj ; that contains changes    
    data = load_data()

    #check for correct patient_id
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    #if patient exists
    existing_patient_info = data[patient_id] #retrieve patient info

    updated_patient_info = patient_update.model_dump(exclude_unset=True) #exclude unset= true bcz we only want updated values saari values patient ki nhi

    for key, value in updated_patient_info.items():
        #in dict {key(city), value(delhi)} jo new aya h; run loop jitne items ho updated me 
        existing_patient_info[key] = value
        #existing wale ki key (city) -> ka value (delhi->kota) update krdo
    
    #existing patient_info (dictionary) -> create Patient class ka a new pydantic object -> has @computed fields -> auto calculate bmi + verdict again
    existing_patient_info['id'] = patient_id #bcz existig_patient_info m id nhi h so add new key-> id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # pydantic obj -> which is a dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    #add dict to data
    data[patient_id] = existing_patient_info

    #save data (in json format)
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient info updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    #load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    del data[patient_id]

    #save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted'})










