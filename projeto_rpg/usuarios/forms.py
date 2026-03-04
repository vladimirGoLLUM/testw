from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, IntegerField,
                    TextAreaField, BooleanField, ValidationError)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                NumberRange, ValidationError)
from projeto_rpg.models_db import Usuario
from flask_login import current_user
from flask_babel import _  # Импортируем функцию перевода


class Mensagem_erro(object):

    def erro_tamanho(self, min_val, max_val):
        return _('Должно быть от {min} до {max} символов').format(min=min_val, max=max_val)

    def erro_obrigatorio(self):
        return _('Это поле обязательно для заполнения')

    def erro_entre(self, comeco, final):
        return _('Значение должно быть между {start} и {end}').format(start=comeco, end=final)


erros = Mensagem_erro()

# Форма регистрации нового пользователя
class Form_Registrar_Usuario(FlaskForm):
    nome = StringField(_('Имя пользователя:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3, 33))])

    email = StringField(_('Электронная почта:'),
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    Email(message=_('Введите действительный адрес электронной почты'))])

    senha = PasswordField(_('Пароль:'),
                          validators=[DataRequired(message=erros.erro_obrigatorio()),
                                      Length(min=5, max=33, message=erros.erro_tamanho(5, 33))])

    confirmar_senha = PasswordField(_('Подтвердите пароль:'),
                                    validators=[DataRequired(message=erros.erro_obrigatorio()),
                                                Length(min=5, max=33),
                                                EqualTo('senha', message=_('Пароли должны совпадать'))])

    foto = FileField(_('Изменить фото профиля:'), validators=[
                     FileAllowed(['jpg', 'jpeg', 'png', 'gif'], _('Разрешены только изображения (JPG, PNG, GIF)'))])

    botao_registrar = SubmitField(_('Зарегистрироваться'))

    def validate_nome(self, nome):
        if Usuario.query.filter_by(nome=nome.data).first():
            raise ValidationError(_('Имя пользователя уже занято. Пожалуйста, выберите другое.'))

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            raise ValidationError(_('Электронная почта уже используется. Пожалуйста, используйте другую.'))


# Форма входа пользователя
class Form_Logar_Usuario(FlaskForm):
    nome = StringField(_('Имя пользователя:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3, 33))])

    senha = PasswordField(_('Пароль:'),
                          validators=[DataRequired(message=erros.erro_obrigatorio()),
                                      Length(min=5, max=33, message=erros.erro_tamanho(5, 33))])

    permanecer_logado = BooleanField(_('Оставаться в системе'))

    botao_logar = SubmitField(_('Войти'))


# Форма редактирования данных пользователя
class Form_Editar_Conta(FlaskForm):
    nome = StringField(_('Новое имя пользователя:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3, 33))])

    email = StringField(_('Новая электронная почта:'),
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    Email(message=_('Введите действительный адрес электронной почты'))])

    imagem_perfil = FileField(_('Изменить фото профиля:'), validators=[
                              FileAllowed(['jpg', 'jpeg', 'png', 'gif'], _('Разрешены только изображения (JPG, PNG, GIF)'))])

    botao_editar = SubmitField(_('Сохранить изменения'))

    def validate_nome(self, nome):
        if nome.data != current_user.nome:
            if Usuario.query.filter_by(nome=nome.data).first():
                raise ValidationError(_('Имя пользователя уже занято. Пожалуйста, выберите другое.'))

    def validate_email(self, email):
        if email.data != current_user.email:
            if Usuario.query.filter_by(email=email.data).first():
                raise ValidationError(_('Электронная почта уже используется. Пожалуйста, используйте другую.'))


# Форма запроса восстановления пароля
class Form_Requisitar_Recuperacao(FlaskForm):
    email = StringField(_('Электронная почта аккаунта:'),
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    Email(message=_('Введите действительный адрес электронной почты'))])

    botao_requisitar = SubmitField(_('Запросить'))

    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first() is None:
            raise ValidationError(_('Этот адрес электронной почты не зарегистрирован. Попробуйте другой.'))


# Форма смены пароля
class Form_Alterar_Senha(FlaskForm):
    senha = PasswordField(_('Пароль:'),
                          validators=[DataRequired(message=erros.erro_obrigatorio()),
                                      Length(min=5, max=33, message=erros.erro_tamanho(5, 33))])

    confirmar_senha = PasswordField(_('Подтвердите пароль:'),
                                    validators=[DataRequired(message=erros.erro_obrigatorio()),
                                                Length(min=5, max=33),
                                                EqualTo('senha', message=_('Пароли должны совпадать'))])

    botao_enviar = SubmitField(_('Изменить'))