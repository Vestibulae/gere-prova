from flask import Flask, request
from flask.json import jsonify
from util.controller import getProvaPronta
from flask_cors import CORS
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/v1/gerarprova')
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


app.run()
