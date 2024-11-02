from ..models.appointments_model import Appointments
from ..models.available_slots_model import AvailableSlots
from ..models.user_model import User
from ..models.doctor_model import Doctor
from ..models.health_unity_model import HealthUnity
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from pymongo import MongoClient
from ..config import Config
from bson import ObjectId
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .available_slots_service import delete_available_slots

import re

client = MongoClient(Config.MONGO_URI)
db = client['agendeja_db']
ap_collection = db['appointments']
as_collection = db['available_slots']
us_collection = db['users']
doctors_collection = db['doctors']
health_unity = db['health_unity']

def sendMail(mailTo, mailData):
    html_body = f"""
    <html>
    <body style="position: relative; min-height: 100vh;">
        <section>
            <section style="border-bottom: 2px solid black; margin-bottom: 32px;">
                <section style="width: 100%; max-width: 600px; margin: auto;">
                    <div>
                        <h1
                            style="text-align: center; font-size: 2em; font-family: Arial, Helvetica, sans-serif; color: #081F4B;">
                            <span style="color: #00B3F2;">CONFIRMAÇÃO DE</span> CONSULTA</h1>
                    </div>
                </section>
            </section>
        </section>
        <section style="width: 100%; max-width: 600px; margin: auto; font-family: Arial, Helvetica, sans-serif; border: 2px solid black; padding: 16px; border-radius: 16px;">
            <div>
                <strong style="font-size: 1.5em;">N°: </strong><span style="font-size: 1.2em;">{mailData['id']}</span>
            </div>
            <div>
                <strong style="font-size: 1.5em;">Nome Paciente: </strong><span style="font-size: 1.2em;">{mailData['nome_paciente']}</span>
            </div>
            <div>
                <strong style="font-size: 1.5em;">CPF: </strong><span style="font-size: 1.2em;">{mailData['cpf']}</span>
            </div>
            <div>
                <strong style="font-size: 1.5em;">Local: </strong><span style="font-size: 1.2em;">{mailData['local']}</span>
            </div>
            <div>
                <strong style="font-size: 1.5em;">Data e Hora: </strong><span style="font-size: 1.2em;">{mailData['data_hora']}</span>
            </div>
            <div>
                <strong style="font-size: 1.5em;">Dr(a).: </strong><span style="font-size: 1.2em;">{mailData['dr']}</span>
            </div>
        </section>
        <footer style="width: 100%; max-width: 600px; margin: auto; font-family: Arial, Helvetica, sans-serif; background-color: #081F4B; position: absolute; bottom: 0; left: 50%; transform: translate(-50%, -100%); text-align: center;">
            <p style="color: white; font-size: 1.2em; padding: 0 12px;">Agradecemos sua consulta.</p>
        </footer>
    </body>
    </html>
    """
    
    sender = Config.SENDER
    password = Config.PASSWORD
    
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(sender, password)

    mensagem = MIMEMultipart()
    mensagem["From"] = sender
    mensagem["To"] = mailTo
    mensagem["Subject"] = Config.SUBJECT
    mensagem.attach(MIMEText(html_body, "html"))

    servidor.send_message(mensagem)
    servidor.quit()

def post_appointments(data):
    mail = data['paciente_email']
    
    vaga = as_collection.find_one({"_id": ObjectId(data["vaga_id"])})
    
    if not vaga:
        return {"error": "Vaga não encontrada"}, 404
    
    user = us_collection.find_one({"_id": ObjectId(data["usuario_id"])})
    
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    
    doctor = doctors_collection.find_one({"_id": vaga["medico_id"]})
    unity = health_unity.find_one({"_id": vaga["unidade_id"]})

    user_data = User(**user).dict(by_alias=True)
    doctor_data = Doctor(**doctor).dict(by_alias=True) if doctor else None
    unity_data = HealthUnity(**unity).dict(by_alias=True) if unity else None

    available_slot = AvailableSlots(
        id=vaga["_id"],
        data=vaga["data"],
        horario=vaga["horario"],
        medico=doctor_data,
        unidade=unity_data
    )
    
    if not available_slot.id:
        available_slot.id = str(vaga['_id'])

    appointment_data = {
        "usuario": user_data,
        "vaga": available_slot,
        "paciente_nome": data["paciente_nome"],
        "paciente_data": data["paciente_data"],
        "paciente_cpf": data["paciente_cpf"],
        "paciente_tel": data["paciente_tel"],
        "paciente_email": data["paciente_email"],
        "paciente_rg": data["paciente_rg"],
    }

    try:
        appointment_instance = Appointments(**appointment_data)
        result = ap_collection.insert_one(appointment_instance.dict(by_alias=True))
        
        id = re.sub(r'\D', '', str(result.inserted_id))
        
        dataFormatted = appointment_data['vaga'].data.strftime('%d/%m/%Y')
        data_hora = f"{dataFormatted}-{appointment_data['vaga'].horario}"

        mailData = {
            "id": id,
            "nome_paciente": data['paciente_nome'],
            "cpf": data['paciente_cpf'],
            "local": appointment_data['vaga'].unidade.endereco,
            "data_hora": data_hora,
            "dr": appointment_data['vaga'].medico.nome
        }
        
        if id:
            sendMail(mail, mailData)
            delete_available_slots({'id': data['vaga_id']})
            
        
        return {"message": "Agendamento criado com sucesso!", "id": id}

    except ValidationError as ve:
        return {"error": "Erro de validação", "Detalhes": ve.errors()}

    except PyMongoError as pe:
        return {"error": "Erro ao inserir no banco de dados", "Detalhes": str(pe)}

    except Exception as e:
        return {"error": "Erro inesperado aconteceu", "Detalhes": str(e)}