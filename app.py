import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests #tem que instalar
import json

# Caminho completo para o arquivo de chave de API
caminho_chave_api = os.path.abspath("silicon-mile-375220-8289a0d58a0b.json")

# Carregando as credenciais
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(caminho_chave_api, scope)

# Autorizando o acesso
client = gspread.authorize(credentials)

# Abrindo uma planilha pelo nome
spreadsheet = client.open('Reservas_do_Salão_de_Cabeleireiro')

# Acessando uma aba específica pelo índice
worksheet = spreadsheet.get_worksheet(0)  # Supondo que a planilha tenha apenas uma aba

# Obtenha a data e hora atuais
data_hora_atual = datetime.now().month
data_ano = datetime.now().year

dataemes = f'/{data_hora_atual}/{data_ano}'


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    data = request.get_json(silent=True)

    #print(data)
    intentName = data['queryResult']['intent']['displayName']
    nome = data['queryResult']['parameters']['nome']
    datadia = data['queryResult']['parameters']['data']
    horario = data['queryResult']['parameters']['hora']

#intentName marcar
    if intentName == "marcar":

        data['fulfillmentText'] = f"Ok Sr(a) {nome}, sua reserva \
foi registrada no dia {datadia} as {horario} horas."

    nova_linha = [nome, datadia+dataemes, horario]
    worksheet.append_row(nova_linha)
        
    return jsonify(data)

#iniciar o Flask app:
if __name__ == "__main__":
    app.debug = False
    app.run()

    