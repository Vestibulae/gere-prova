from flask import Flask, request
from flask import json
from flask.json import jsonify
from util.controller import getProvaPronta
from flask_cors import CORS
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/v1/gerarprova', methods=['GET', 'POST'])
def gerarProva():
    json_data = request.get_json(force=True)

    prova = "" if not 'prova' in json_data else json_data['prova']
    ano = "" if not 'ano' in json_data else json_data['ano']
    fase = "" if not 'fase' in json_data else json_data['fase']
    materia = [] if not 'materia' in json_data else json_data['materia']
    nQuestoes = 10 if not 'numero_questoes' in json_data else int(
        json_data['numero_questoes'])

    return jsonify(getProvaPronta(prova=prova, ano=ano, fase=fase, materia=materia, nQuestoes=nQuestoes))


# @app.route('/pesquisa/<nome>')
# def pesquisa(nome):
#     return jsonify(select(nome))


# @app.route('/aluno/<id>')
# def aluno(id):
#     return jsonify(getById(id))


# @app.route('/insere', methods=['POST'])
# def insere():
#     json_data = request.get_json(force=True)
#     nome = json_data["nome"]
#     idade = json_data["idade"]
#     aluno = Alunos(nome=nome, idade=idade)
#     return inserir(aluno)


# @app.route('/deletar', methods=['DELETE'])
# def deletar():
#     id = request.args.get("id")
#     return delete(id)


# @app.route('/atualizar', methods=['PUT'])
# def atualizar():
#     id = request.form.get("id")
#     nome = request.form.get("nome")
#     idade = request.form.get("idade")
#     aluno = Alunos(id=id, nome=nome, idade=idade)
#     return update(aluno)

# print(getProvaPronta(nQuestoes=2, materia=[
#       "Portugues", "matematica", "biologia"], ano="", prova="", fase=""))


app.run(port=8090)
