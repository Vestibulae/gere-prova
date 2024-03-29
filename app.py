from flask import Flask, json, request, jsonify
from peewee import DoesNotExist
from util.controller import corrige, getAcertos, getProvaPronta
from flask_cors import CORS
from util.models import Acertos

DADOS_INVALIDOS = {"success": False, "message": "Dados Invalidos!"}

app = Flask(__name__)
app.config["DEBUG"] = True
# CORS(app)


@app.route('/api/v1/gerarprova', methods=['GET', 'POST'])
def gerarProva():
    json_data = request.get_json(force=True)

    prova = "" if not 'prova' in json_data else json_data['prova']
    ano = "" if not 'ano' in json_data else json_data['ano']
    fase = "" if not 'fase' in json_data else json_data['fase']
    materia = [] if not 'materia' in json_data else json_data['materia']
    nQuestoes = 10 if not 'numero_questoes' in json_data or json_data['numero_questoes'] == "" or json_data['numero_questoes'] == 0 else int(
        json_data['numero_questoes'])

    return jsonify(getProvaPronta(prova=prova, ano=ano, fase=fase, materia=materia, nQuestoes=nQuestoes))


@app.route('/api/v1/corrigirprova', methods=['GET', 'POST'])
def corrigirProva():
    json_data = request.get_json(force=True)
    try:
        usuario = json_data['usuario']
        gabaritos = json_data['gabaritos']
        respostas_usuario = json_data['respostas_usuario']
        correcao = corrige(usuario=usuario, gabaritos=gabaritos,
                           respostas_usuario=respostas_usuario)
    except DoesNotExist:
        return jsonify(DADOS_INVALIDOS), 404
    except Exception:
        return jsonify(DADOS_INVALIDOS), 400

    return jsonify(correcao)


@app.route('/api/v1/dadosgraficos', methods=['GET', 'POST'])
def dadosGraficos():
    json_data = request.get_json(force=True)
    try:
        usuario = json_data['usuario']
        dados = getAcertos(usuario=usuario)

    except DoesNotExist:
        return jsonify(DADOS_INVALIDOS), 404
    except Exception:
        return jsonify(DADOS_INVALIDOS), 400

    return jsonify(dados)


Acertos.create_table()
app.run(port=8090)
