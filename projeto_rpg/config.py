import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bd023b5638a8f04016fdedf53a2f3736'

    # Используем PostgreSQL, если доступен, иначе SQLite (для локальной разработки)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///rpg.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Configuração para o envio de e-mails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'projeto.rpg.suporte@gmail.com'
    #Senha apenas funciona para o acesso desse APP
    MAIL_PASSWORD = 'vxybiaiaiettlywz'
    MAIL_DEFAULT_SENDER='projeto.rpg.suporte@gmail.com'