from ..models.available_slots_model import AvailableSlots
from ..models.doctor_model import Doctor
from ..models.health_unity_model import HealthUnity
from pymongo import MongoClient
from ..config import Config
from bson import ObjectId
from bson.errors import InvalidId

client = MongoClient(Config.MONGO_URI)
db = client['agendeja_db']
as_collection = db['available_slots']
doctors_collection = db['doctors']
unidades_collection = db['health_unity']

def get_available_slots():
    available_slots = as_collection.find()
    result = []

    for slot in available_slots:
        doctor = doctors_collection.find_one({"_id": slot["medico_id"]})
        doctor_data = Doctor(**doctor).dict(by_alias=True) if doctor else None

        unity = unidades_collection.find_one({"_id": slot["unidade_id"]})
        unity_data = HealthUnity(**unity).dict(by_alias=True) if unity else None

        slot_data = AvailableSlots(
            id=slot["_id"],
            data=slot["data"],
            horario=slot["horario"],
            medico=doctor_data,
            unidade=unity_data
        )

        if not slot_data.id:
            slot_data.id = str(slot['_id'])
            
        result.append(slot_data.dict(by_alias=True))

    return result

def delete_available_slots(data):
    try:
        id = ObjectId(data['id'])
        result = as_collection.find_one_and_delete({'_id': id})
        
        if result is None:
            return {"error": "Nenhuma vaga encontrada com esse ID"}
        
        return {"success": "Vaga deletada com sucesso"}
    
    except InvalidId:
        return {"error": "ID inválido. Certifique-se de que está no formato correto"}
    
    except Exception as e:
        return {"error": f"Ocorreu um erro: {str(e)}"}
