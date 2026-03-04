from flask import Flask, request, jsonify, render_template
from motor import MotorIA

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():

    dados = request.json
    motor = MotorIA(dados['versao'])
    resultado = motor.gerar_conteudo(dados['indice_aluno'], dados['topico'], dados['tipo_conteudo'], dados['precisao'])

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)