from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime
from doctor_model import Doctor
from health_unity_model import HealthUnity

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)
    
class AvailableSlots(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    data: datetime
    horario: str
    medico: Doctor
    unidade: HealthUnity