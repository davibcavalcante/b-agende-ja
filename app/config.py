import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Davi:sRYsfWquYimSXBYP@cluster0.6psnp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'PALFHSDLSDKAFNASDOIWODSÇALDKFJDKHGADÇKLFAHDHA')
    SENDER = os.getenv('SENDER', 'indigitalsendmailer@gmail.com')
    PASSWORD = os.getenv('PASSWORD', 'wofq gwkw ctro pxye')
    SUBJECT = os.getenv('SUBJECT', 'AGENDE JÁ - CONFIMRAÇÃO DE CONSULTA')