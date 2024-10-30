from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)
    
class Doctor(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    unidade_id: Optional[PyObjectId] = Field(alias="unidade_id")
    nome: str