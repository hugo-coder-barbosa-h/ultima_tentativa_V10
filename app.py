import os

from flask import Flask, request
from tchan import ChannelScraper
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import date, timedelta

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
bot = telegram.Bot(token=os.environ["TELEGRAM_API_KEY"])
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1srTpWeSZKLAxMcw_OqhKmzEJxwDPjP7jhvvNGudtx-E")
sheet = planilha.worksheet("Página1")

app = Flask(__name__)

menu = """ 
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/promocoes">PROMOÇÕES</a>  
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, este é o site do robô sobre PLs aprovadas."

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"

@app.route("/promocoes2")
def promocoes2():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  scraper = ChannelScraper()
  contador = 0
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    conteudo += f"<li>{message.created_at} {texto}</li>"
    if contador == 10:
      break
  return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["HUGO", "H", "a partir do Flask"])
  return "Planilha escrita!"

@app.route('/projetos_aprovados')
def projetos_aprovados():
    hoje = date.today().strftime('%Y-%m-%d')
    ontem = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={ontem}&dataFim={hoje}&siglaTipo=PL&ordenarPor=ano"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        projetos_aprovados = []
        projetos_dict = []
        df = pd.DataFrame(columns=['ID', 'Tipo', 'Número', 'Ementa'])
        if dados['dados']:
            for projeto in dados['dados']:
                projetos_aprovados.append(f"{projeto['siglaTipo']} {projeto['numero']} - {projeto['ementa']}")
                df = df.append({'ID': projeto['id'], 'Tipo': projeto['siglaTipo'], 'Número': projeto['numero'], 'Ementa': projeto['ementa']}, ignore_index=True)
        return render_template('projetos.html', projetos=df.to_html())
    else:
        return f"Error: {response.status_code}"
      
  
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {
    "chat_id": chat_id,
    "text": f"Você enviou a mensagem: <b>{message}</b>",
    "parse_mode": "HTML",
  }
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  print(resposta.text)
  return "ok"


@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]

    if message.lower() == '1':
        nova_mensagem = {
            "chat_id": chat_id,
            "text": "Opção 1 selecionada.",
        }
    elif message.lower() == '2':
        nova_mensagem = {
            "chat_id": chat_id,
            "text": "Opção 2 selecionada.",
        }
    elif message.lower() == '3':
        nova_mensagem = {
            "chat_id": chat_id,
            "text": "Opção 3 selecionada.",
        }
    else:
        nova_mensagem = {
            "chat_id": chat_id,
            "text": "Olá! Por favor, escolha uma das opções abaixo:\n1. Opção 1\n2. Opção 2\n3. Opção 3",
        }
    
    resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    print(resposta.text)
    return "ok"



      


  
  



                                                                
                                                                
