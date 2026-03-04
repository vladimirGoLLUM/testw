from flask import Blueprint, render_template
from PIL import Image
from projeto_rpg.models_db import Personagem
from projeto_rpg import app, db
from flask_babel import _  # Импортируем функцию перевода
import secrets
import os

geral = Blueprint('geral', __name__)

# Маршрут на главную страницу
@geral.route("/")
@geral.route("/home")
def mostrar_home():
    personagens = Personagem.query.order_by(Personagem.data_criacao.desc()).limit(6)
    return render_template('home.html', personagens=personagens, titulo=_('Главная'))

# Метод для сохранения сжатых изображений
def salvar_imagem(diretorio, form_picture):
    rhex = secrets.token_hex(9)
    _, foto_ext = os.path.splitext(form_picture.filename)
    nome_foto = rhex + foto_ext
    caminho = os.path.join(app.root_path, diretorio, nome_foto)

    # Изменение размера изображения перед загрузкой (если не GIF)
    if foto_ext.lower() != '.gif':
        tamanho_imagem = (200, 200)
        imagem_menor = Image.open(form_picture)
        imagem_menor.thumbnail(tamanho_imagem)
        imagem_menor.save(caminho)
    else:
        form_picture.save(caminho)
    return nome_foto

# Метод для удаления изображений при удалении пользователя или персонажа
def apagar_imagem(diretorio, foto):
    caminho = os.path.join(app.root_path, diretorio, foto)
    if os.path.exists(caminho):
        os.remove(caminho)