from util.db import db
from peewee import *
from util.models import Acertos, Provas, Questoes, Respostas, Usuarios
from datetime import datetime
#
#
#
###### seção para geração da prova ######
#
#
#


def getProvas(nome_prova, ano, fase):
    with db.atomic() as trans:
        try:
            provas = list(Provas.select().where(
                Provas.prova ** f"%{nome_prova}%", Provas.ano ** f"%{ano}%", Provas.fase ** f"%{fase}%"))
            trans.commit()

            return provas
        except Provas.DoesNotExist as err:
            print(err, f"data: {nome_prova}, {ano}, {fase}")


def getQuestoes(provas, materia, nQuestoes):
    with db.atomic() as trans:
        try:
            if materia:
                questoes = Questoes.select().where(Questoes.prova_id << provas, Questoes.materia <<
                                                   materia).order_by(fn.Rand()).limit(nQuestoes)
            else:
                questoes = Questoes.select().where(
                    Questoes.prova_id << provas).order_by(fn.Rand()).limit(nQuestoes)
            trans.commit()
            return questoes
        except Questoes.DoesNotExist as err:
            print(err, f"data: {provas}, {materia}, {nQuestoes}")


def getProvaPronta(prova, ano, fase, materia, nQuestoes):

    provas = getProvas(nome_prova=prova, ano=ano, fase=fase)
    id_provas = [p.id for p in provas]

    questoes = getQuestoes(
        provas=id_provas, materia=materia, nQuestoes=int(nQuestoes))

    questoes_json = []
    respostas_json = []
    gabaritos_json = []
    for q in questoes:
        questoes_json.append({"id": q.id, "prova_id": q.prova_id.id, "numero": int(q.numero), "materia": q.materia,
                              "enunciado": q.enunciado, "assunto": q.assunto, "imagem": q.imagem})

        respostas_json.append([{"id": r.id, "prova_id": r.prova_id.id, "questao_id": r.questao_id.id,
                                "enunciado": r.enunciado, "alternativa": r.alternativa, "imagem": r.imagem} for r in q.respostas])

        gab = q.gabarito.get()
        gabaritos_json.append({"questao_id": gab.questao_id.id,
                               "resposta_id": gab.resposta_id.id})

    json = {"questoes": questoes_json,
            "respostas": respostas_json, "gabaritos": gabaritos_json}

    return json
#
#
#
###### seção para correção e inserção dos acertos da prova ######
#
#
#


def getAlternativa(id_resposta):
    with db.atomic() as trans:
        try:
            alternativa = Respostas.get_by_id(id_resposta).alternativa
            trans.commit()
            return alternativa
        except Respostas.DoesNotExist as err:
            print(err, f"data: {id_resposta}")


def corrige(usuario, gabaritos, respostas_usuario):
    timestamp = datetime.now()
    todos_acertos = []
    for g in gabaritos:
        questao = g['questao_id']
        alternativa_usu = ''
        for r in respostas_usuario:
            if r['questao_id'] == questao:
                alternativa_usu = r['alternativa']
                break

        alternativa_correta = getAlternativa(g['resposta_id'])
        acertou = False
        if alternativa_usu == alternativa_correta:
            acertou = True
        acerto = {"usuario_id": usuario, "questao_id": questao,
                  "acerto": acertou, "data": timestamp}
        todos_acertos.append(acerto)
    insereAcertos(todos_acertos)
    return todos_acertos


def insereAcertos(lista_acertos):
    with db.atomic() as trans:
        try:
            Acertos.insert_many(lista_acertos).execute()
            trans.commit()
        except Usuarios.DoesNotExist as err:
            print(err)
            trans.rollback()
            raise DoesNotExist("Usuario Inexistente!")
        except DatabaseError as err:
            print(err)
            trans.rollback()
            raise DatabaseError("Erro no banco de dados!")
#
#
#
###### seção para puxar os dados para os gráficos ######
#
#
#


def getAcertos(usuario):
    with db.atomic() as trans:
        try:
            acertos = list(Acertos.select().where(
                Acertos.usuario_id == usuario))
            trans.commit()

            return acertos
        except Usuarios.DoesNotExist as err:
            print(err)
            raise DoesNotExist("Usuário Inexistente!")
