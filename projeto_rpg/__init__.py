# Windows = set FLASK_APP=app.py
# Linux = export FLASK_APP=app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from projeto_rpg.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Переместил выше — логичнее до login_manager

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'usuarios.logar_usuario'          # ← исправлено: login_manager
login_manager.login_message_category = 'info'                # ← и здесь

mail = Mail(app)

# Регистрация Blueprints
from projeto_rpg.usuarios.routes import usuarios
app.register_blueprint(usuarios)

from projeto_rpg.personagens.routes import personagens
app.register_blueprint(personagens)

from projeto_rpg.geral.routes import geral
app.register_blueprint(geral)

from projeto_rpg.erros.handlers import erros
app.register_blueprint(erros)

with app.app_context():
    db.create_all()