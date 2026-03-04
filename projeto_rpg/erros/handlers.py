from flask import Blueprint, render_template
from flask_babel import _  # Импортируем функцию перевода

erros = Blueprint('erros', __name__)

@erros.app_errorhandler(403)
def erro_403(error):
    # Можно передать заголовок и описание в шаблон
    return render_template('erros/erro_403.html',
                           titulo=_('Доступ запрещён'),
                           mensagem=_('У вас нет прав для просмотра этой страницы.')), 403

@erros.app_errorhandler(404)
def erro_404(error):
    return render_template('erros/erro_404.html',
                           titulo=_('Страница не найдена'),
                           mensagem=_('Извините, страница, которую вы ищете, не существует.')), 404

@erros.app_errorhandler(500)
def erro_500(error):
    return render_template('erros/erro_500.html',
                           titulo=_('Внутренняя ошибка сервера'),
                           mensagem=_('Что-то пошло не так на сервере. Попробуйте позже.')), 500