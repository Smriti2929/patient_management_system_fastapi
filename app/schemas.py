from pydantic import BaseModel, Field
from typing import Literal, Optional

class PatientBase(BaseModel):
    name: str = Field(..., description= "Patient name")
    city: str
    age: int = Field(..., gt=0, lt=120)
    gender: Literal["male", "female", "others"]
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)

class PatientCreate(PatientBase):
    id: str

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120) 
    gender: Optional[Literal["male", "female", "others"]] = None
    height: Optional[float] = Field(default=None, gt=0) 
    weight: Optional[float] = Field(default=None, gt=0)

class PatientResponse(PatientBase):
    id: str
    bmi: float
    verdict: str

    model_config = {
        "from_attributes": True
    }         