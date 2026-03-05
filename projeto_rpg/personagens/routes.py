from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from projeto_rpg.personagens.forms import Form_Personagem, Form_Procurar_Personagem, Form_Avaliar_Personagem
from projeto_rpg.models_db import Personagem, Avaliacao
from projeto_rpg import app, db
from flask_login import current_user, login_required
from projeto_rpg.geral.routes import salvar_imagem, apagar_imagem
from datetime import datetime
from flask_babel import _


personagens = Blueprint('personagens', __name__)


@personagens.route("/registrar_personagem", methods=['GET', 'POST'])
@login_required
def registrar_personagem():
    form_personagem = Form_Personagem()

    if form_personagem.validate_on_submit():
        if form_personagem.foto_referencia.data:
            picture_file = salvar_imagem('static/imagens_personagens', form_personagem.foto_referencia.data)
            form_personagem.foto_referencia.data = picture_file

        novo_personagem = Personagem(
            nome=form_personagem.nome.data,
            raca=form_personagem.raca.data,
            classe=form_personagem.classe.data,
            nivel=form_personagem.nivel.data,
            forca=form_personagem.forca.data,
            destreza=form_personagem.destreza.data,
            constituicao=form_personagem.constituicao.data,
            inteligencia=form_personagem.inteligencia.data,
            sabedoria=form_personagem.sabedoria.data,
            carisma=form_personagem.carisma.data,
            historia=form_personagem.historia.data,
            foto=form_personagem.foto_referencia.data,
            autor=current_user
        )

        db.session.add(novo_personagem)
        db.session.commit()
        flash(_('Персонаж успешно зарегистрирован!'), 'success')
        return redirect(url_for('geral.mostrar_home'))

    return render_template('registrar_personagem.html',
                           titulo=_('Зарегистрировать персонажа'),
                           form_personagem=form_personagem)


@personagens.route("/personagem/<int:personagem_id>", methods=['GET', 'POST'])
def mostrar_personagem(personagem_id):
    pagina = request.args.get('pagina', 1, type=int)
    personagem = Personagem.query.get_or_404(personagem_id)

    if current_user.is_authenticated:
        avaliacoes = Avaliacao.query.filter(
            Avaliacao.autor_id != current_user.id,
            Avaliacao.personagem_id == personagem_id
        ).paginate(page=pagina, per_page=6)
        avaliacao_usuario = Avaliacao.query.filter_by(
            autor_id=current_user.id, personagem_id=personagem_id).first()
    else:
        avaliacao_usuario = None
        avaliacoes = Avaliacao.query.filter_by(
            personagem_id=personagem_id).paginate(page=pagina, per_page=6)

    # ✅ Правильный расчёт средней оценки
    notas = [a.nota for a in avaliacoes.items]
    if avaliacao_usuario:
        notas.append(avaliacao_usuario.nota)

    if notas:
        personagem.nota = round(sum(notas) / len(notas), 2)
    else:
        personagem.nota = None

    db.session.commit()

    form_avaliar = Form_Avaliar_Personagem()
    form_editar_avaliacao = Form_Avaliar_Personagem()

    if avaliacao_usuario and form_editar_avaliacao.validate_on_submit():
        avaliacao_usuario.data_postagem = datetime.now(timezone.utc)
        avaliacao_usuario.conteudo = form_editar_avaliacao.conteudo.data
        avaliacao_usuario.nota = form_editar_avaliacao.nota.data
        db.session.commit()
        flash(_('Оценка успешно изменена!'), 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    elif form_avaliar.validate_on_submit():
        nova_avaliacao = Avaliacao(
            autor_id=current_user.id,
            personagem_id=personagem_id,
            conteudo=form_avaliar.conteudo.data,
            nota=form_avaliar.nota.data
        )
        db.session.add(nova_avaliacao)
        db.session.commit()
        flash(_('Персонаж успешно оценён!'), 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    elif request.method == "GET" and avaliacao_usuario:
        form_editar_avaliacao.nota.data = avaliacao_usuario.nota
        form_editar_avaliacao.conteudo.data = avaliacao_usuario.conteudo

    return render_template(
        'personagem.html',
        titulo=personagem.nome,
        personagem=personagem,
        avaliacoes=avaliacoes,
        form_avaliar=form_avaliar,
        form_editar_avaliacao=form_editar_avaliacao,
        avaliacao_usuario=avaliacao_usuario
    )


@personagens.route("/personagem/<int:personagem_id>/apagar_avaliacao/<int:autor_id>", methods=['POST'])
@login_required
def apagar_avaliacao(personagem_id, autor_id):
    avaliacao = Avaliacao.query.get_or_404((autor_id, personagem_id))
    personagem = Personagem.query.get_or_404(personagem_id)

    if (avaliacao.autor != current_user) and not current_user.isAdmin:
        abort(403)

    db.session.delete(avaliacao)
    db.session.commit()

    # ✅ Пересчитываем оценку
    todas_aval = Avaliacao.query.filter_by(personagem_id=personagem_id).all()
    notas = [a.nota for a in todas_aval]
    personagem.nota = round(sum(notas) / len(notas), 2) if notas else None
    db.session.commit()

    flash(_('Оценка успешно удалена!'), 'success')
    return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem_id))


@personagens.route("/personagem/<int:personagem_id>/editar", methods=['GET', 'POST'])
@login_required
def editar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)

    if (personagem.autor != current_user) and not current_user.isAdmin:
        abort(403)

    form_editar = Form_Personagem()

    if form_editar.validate_on_submit():
        personagem.nome = form_editar.nome.data
        personagem.raca = form_editar.raca.data
        personagem.classe = form_editar.classe.data
        personagem.nivel = form_editar.nivel.data
        personagem.forca = form_editar.forca.data
        personagem.destreza = form_editar.destreza.data
        personagem.constituicao = form_editar.constituicao.data
        personagem.inteligencia = form_editar.inteligencia.data
        personagem.sabedoria = form_editar.sabedoria.data
        personagem.carisma = form_editar.carisma.data
        personagem.historia = form_editar.historia.data

        if form_editar.foto_referencia.data:
            if personagem.foto != 'personagem.png':
                apagar_imagem('static/imagens_personagens', personagem.foto)
            picture_file = salvar_imagem('static/imagens_personagens', form_editar.foto_referencia.data)
            personagem.foto = picture_file

        db.session.commit()
        flash(_('Персонаж успешно изменён!'), 'success')
        return redirect(url_for('personagens.mostrar_personagem', personagem_id=personagem.id))

    elif request.method == "GET":
        # ✅ Правильное заполнение формы
        form_editar.nome.data = personagem.nome
        form_editar.raca.data = personagem.raca
        form_editar.classe.data = personagem.classe
        form_editar.nivel.data = personagem.nivel
        form_editar.forca.data = personagem.forca
        form_editar.destreza.data = personagem.destreza
        form_editar.constituicao.data = personagem.constituicao
        form_editar.inteligencia.data = personagem.inteligencia
        form_editar.sabedoria.data = personagem.sabedoria
        form_editar.carisma.data = personagem.carisma
        form_editar.historia.data = personagem.historia

    return render_template(
        'editar_personagem.html',
        titulo=_('Редактировать персонажа'),
        form_editar=form_editar,
        personagem=personagem
    )


@personagens.route("/personagem/<int:personagem_id>/apagar", methods=['POST'])
@login_required
def apagar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    if (personagem.autor != current_user) and not current_user.isAdmin:
        abort(403)

    avaliacoes = Avaliacao.query.filter_by(personagem_id=personagem_id)
    for avaliacao in avaliacoes:
        db.session.delete(avaliacao)

    if personagem.foto != 'personagem.png':
        apagar_imagem('static/imagens_personagens', personagem.foto)

    db.session.delete(personagem)
    db.session.commit()
    flash(_('Персонаж успешно удалён!'), 'success')
    return redirect(url_for('geral.mostrar_home'))


@personagens.route("/procurar_personagem/", methods=['GET', 'POST'])
def procurar_personagem():
    pagina = request.args.get('pagina', 1, type=int)
    form_procurar_pers = Form_Procurar_Personagem()

    if form_procurar_pers.validate_on_submit():
        personagens = db.session.query(Personagem).filter(
            Personagem.nome.ilike(f"%{form_procurar_pers.nome.data}%"),
            Personagem.raca.ilike(f"%{form_procurar_pers.raca.data}%"),
            Personagem.classe.ilike(f"%{form_procurar_pers.classe.data}%"),
        ).paginate(page=1, per_page=9)
    else:
        personagens = Personagem.query.paginate(page=pagina, per_page=9)

    return render_template(
        'procurar_personagem.html',
        titulo=_('Поиск персонажа'),
        form_procurar_pers=form_procurar_pers,
        personagens=personagens
    )