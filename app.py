from flask import Flask, request
from flask.json import jsonify
from util.controller import getProvaPronta

app = Flask(__name__)
app.config["DEBUG"] = True


# , defaults={"prova": "", "ano": "", "fase": "", "materia": "", "numero_questoes": 10})
@app.route('/gerarprova')
def gerarProva():
    prova = "" if request.args.get(
        'prova') == None else request.args.get('prova')
    ano = "" if request.args.get('ano') == None else request.args.get('ano')
    fase = "" if request.args.get('fase') == None else request.args.get('fase')
    materia = "" if request.args.get(
        'materia') == None else request.args.get('materia')
    nQuestoes = 10 if request.args.get(
        'numero_questoes') == None else request.args.get('numero_questoes')
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


app.run()
