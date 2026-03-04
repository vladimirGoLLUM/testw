# Windows = set FLASK_APP=app.py
# Linux = export FLASK_APP=app.py

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from projeto_rpg.config import Config
from flask_babel import Babel, lazy_gettext as _

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Инициализация Flask-Babel
babel = Babel()
babel.init_app(app)

# Установка языка через g.locale
@app.before_request
def set_language():
    g.locale = 'ru'  # Фиксируем русский язык

# Альтернатива: автоматическое определение
# from flask import request
# def get_locale():
#     return request.accept_languages.best_match(['ru', 'en', 'pt'])
# babel.locale_selector = get_locale

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'usuarios.logar_usuario'
login_manager.login_message_category = 'info'

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