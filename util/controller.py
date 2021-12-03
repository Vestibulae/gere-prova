from util.db import db
from peewee import *
from util.models import Provas, Questoes
# from playhouse.shortcuts import model_to_dict

# def insertProva(prova):
#     with db.atomic() as trans:
#         try:
#             prova.save()
#             trans.commit()
#         except DatabaseError as err:
#             print(err, f"data: {prova}")
#             trans.rollback()


# def insertRespostas(respostas):
#     with db.atomic() as trans:
#         try:
#             Respostas.bulk_create(respostas)
#             trans.commit()
#         except DatabaseError as err:
#             print(err)
#             trans.rollback()


# def insertGabarito(prova_id, questao_id, resposta_id):
#     with db.atomic() as trans:
#         try:
#             Gabaritos.create(prova_id=prova_id,
#                              questao_id=questao_id, resposta_id=resposta_id)
#             trans.commit()
#         except DatabaseError as err:
#             print(err)
#             trans.rollback()


# def insertQuestao(questao):
#     with db.atomic() as trans:
#         try:
#             questao.save()
#             trans.commit()
#             return questao
#         except DatabaseError as err:
#             print(err)
#             trans.rollback()
#             return getQuestao(prova=questao.prova_id, numero=questao.numero, materia=questao.materia)


# def getQuestao(prova, numero, materia):
#     with db.atomic() as trans:
#         try:
#             questao = Questoes.get(Questoes.prova_id == prova, Questoes.numero ==
#                                    numero, Questoes.materia == materia)
#             trans.commit()
#             return questao
#         except Questoes.DoesNotExist as err:
#             print(err, f"data: {prova}, {numero}, {materia}")


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


# def getResposta(prova, questao, alternativa):
#     with db.atomic() as trans:
#         try:
#             resposta = Respostas.get(Respostas.prova_id == prova, Respostas.questao_id ==
#                                      questao, Respostas.alternativa == alternativa).id
#             trans.commit()
#             return resposta
#         except Questoes.DoesNotExist as err:
#             print(err, f"data: {prova}, {questao}, {alternativa}")


# def getRespostas(questoes):
#     with db.atomic() as trans:
#         try:
#             respostas = list(Respostas.select().where(
#                 Respostas.questao_id << questoes).dicts())
#             trans.commit()
#             return respostas
#         except Respostas.DoesNotExist as err:
#             print(err, f"data: {questoes}")


# print(getProvaPronta(nQuestoes=1, materia="Portugues"))
