from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

from .user_model import User
from .available_slots_model import AvailableSlots

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError("Invalid ObjectId")
        try:
            return cls(v)
        except Exception:
            raise ValueError("Invalid ObjectId")
    
class Appointments(BaseModel):
    usuario: User
    vaga: AvailableSlots 
    paciente_nome: str
    paciente_data: str
    paciente_cpf: str
    paciente_tel: str
    paciente_email: str
    paciente_rg: str
    paciente_cns: str