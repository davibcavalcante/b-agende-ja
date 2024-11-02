import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SENDER = os.getenv('SENDER')
    PASSWORD = os.getenv('PASSWORD')
    SUBJECT = os.getenv('SUBJECT', 'AGENDE JÁ - CONFIRMAÇÃO DE CONSULTA')