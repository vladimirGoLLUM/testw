from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from projeto_rpg.models_db import Personagem
from flask_babel import _


class Mensagem_erro(object):

    def erro_tamanho(self, min_val, max_val):
        return _('Должно быть от {min} до {max} символов').format(min=min_val, max=max_val)

    def erro_obrigatorio(self):
        return _('Это поле обязательно для заполнения')

    def erro_entre(self, comeco, final):
        return _('Значение должно быть между {start} и {end}').format(start=comeco, end=final)


erros = Mensagem_erro()


# Форма регистрации персонажа
class Form_Personagem(FlaskForm):
    nome = StringField(_('Имя:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3, 33))])

    raca = StringField(_('Раса:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=2, max=33, message=erros.erro_tamanho(2, 33))])

    classe = StringField(_('Класс:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     Length(min=4, max=33, message=erros.erro_tamanho(4, 33))])

    nivel = IntegerField(_('Уровень:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    forca = IntegerField(_('Сила:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    destreza = IntegerField(_('Ловкость:'),
                            validators=[DataRequired(message=erros.erro_obrigatorio()),
                                        NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    constituicao = IntegerField(_('Телосложение:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                            NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    inteligencia = IntegerField(_('Интеллект:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                            NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    sabedoria = IntegerField(_('Мудрость:'),
                             validators=[DataRequired(message=erros.erro_obrigatorio()),
                                         NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    carisma = IntegerField(_('Харизма:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    historia = TextAreaField(_('История:'),
                             validators=[DataRequired(message=erros.erro_obrigatorio()),
                                         Length(min=30, message=_('Минимум {num} символов').format(num=30))])

    foto_referencia = FileField(_('Изображение персонажа:'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], _('Разрешены только изображения (JPG, PNG, GIF)'))])

    botao_enviar = SubmitField(_('Зарегистрировать'))


# Форма поиска персонажа
class Form_Procurar_Personagem(FlaskForm):
    nome = StringField(_('Имя:'),
                       validators=[Length(max=33, message=erros.erro_tamanho(1, 33))])

    raca = StringField(_('Раса:'),
                       validators=[Length(max=33, message=erros.erro_tamanho(1, 33))])

    classe = StringField(_('Класс:'),
                         validators=[Length(max=33, message=erros.erro_tamanho(1, 33))])

    botao_procurar = SubmitField(_('Поиск'))


# Форма оценки персонажа
class Form_Avaliar_Personagem(FlaskForm):
    nota = IntegerField(_('Оценка (0–5):'),
                        validators=[DataRequired(message=erros.erro_obrigatorio()),
                                    NumberRange(min=0.1, max=5.0, message=erros.erro_entre(0.1, 5.0))])

    conteudo = TextAreaField(_('Ваш отзыв:'),
                             validators=[DataRequired(message=erros.erro_obrigatorio()),
                                         Length(min=5, message=erros.erro_tamanho(5, 9999))])

    botao_avaliar = SubmitField(_('Оценить'))


# Форма редактирования персонажа
class Form_Editar_Personagem(FlaskForm):
    nome = StringField(_('Имя:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=3, max=33, message=erros.erro_tamanho(3, 33))])

    raca = StringField(_('Раса:'),
                       validators=[DataRequired(message=erros.erro_obrigatorio()),
                                   Length(min=2, max=33, message=erros.erro_tamanho(2, 33))])

    classe = StringField(_('Класс:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     Length(min=4, max=33, message=erros.erro_tamanho(4, 33))])

    nivel = IntegerField(_('Уровень:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    forca = IntegerField(_('Сила:'),
                         validators=[DataRequired(message=erros.erro_obrigatorio()),
                                     NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    destreza = IntegerField(_('Ловкость:'),
                            validators=[DataRequired(message=erros.erro_obrigatorio()),
                                        NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    constituicao = IntegerField(_('Телосложение:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                            NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])  # Исправлено: ero_entre → erro_entre

    inteligencia = IntegerField(_('Интеллект:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                            NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    sabedoria = IntegerField(_('Мудрость:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                            NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    carisma = IntegerField(_('Харизма:'),
                                validators=[DataRequired(message=erros.erro_obrigatorio()),
                                             NumberRange(min=1, max=99, message=erros.erro_entre(1, 99))])

    historia = TextAreaField(_('История:'),
                             validators=[DataRequired(message=erros.erro_obrigatorio()),
                                         Length(min=30, message=_('Минимум {num} символов').format(num=30))])

    foto_referencia = FileField(_('Изображение персонажа:'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], _('Разрешены только изображения (JPG, PNG, GIF)'))])

    botao_editar = SubmitField(_('Отправить'))