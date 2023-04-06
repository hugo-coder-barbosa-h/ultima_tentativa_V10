import os


from flask import Flask, request
from tchan import ChannelScraper
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
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
  sheet.append_row(["HUGO", "HENUD", "a partir do Flask"])
  return "Planilha escrita!"

def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def get_projects():
    hoje = date.today().strftime('%Y-%m-%d')
    ontem = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={ontem}&dataFim={hoje}&siglaTipo=PL&ordenarPor=ano"
    response = requests.get(url)
    dados = response.json()
    projetos_aprovados = []
    projetos_dict = []
    df = pd.DataFrame(columns=['ID', 'Tipo', 'Número', 'Ementa'])
    for projeto in dados['dados']:
        projetos_aprovados.append(f"{projeto['siglaTipo']} {projeto['numero']} - {projeto['ementa']}")
        projetos_dict.append({'Tipo': projeto['siglaTipo'], 'Número': projeto['numero'], 'Ementa': projeto['ementa']})
    if dados['dados']:
        for i, projeto in enumerate(projetos_dict):
            row = [i+2, projeto['Tipo'], projeto['Número'], projeto['Ementa']]
            sheet.append_row(row)
    return projetos_aprovados

# Rota do webhook do Telegram
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    # Obter a mensagem enviada pelo usuário
    mensagem = request.get_json()
    chat_id = mensagem["message"]["chat"]["id"]
    text = mensagem["message"]["text"]

    if text.lower() == '1':
        # Obter os projetos de lei aprovados
        projetos_aprovados = get_projects()

        if projetos_aprovados:
            # Enviar a lista de projetos de lei para o usuário
            send_message(chat_id, "Projetos de Lei aprovados:\n" + "\n".join(projetos_aprovados))
        else:
            send_message(chat_id, "Não foram encontrados projetos de lei aprovados nos últimos dois dias.")
    elif text.lower() == '2':
        # Enviar o link para o site da Câmara dos Deputados
        bot.send_message(chat_id=chat_id, text="Acesse o site da Câmara dos Deputados para mais detalhes: https://www.camara.leg.br/busca-portal/projetoslegislativos/")
    else:
      mensagem = "Olá, aqui você tem acesso aos Projetos de Lei aprovados na Câmara dos Deputados. Escolha uma das opções abaixo:\n"
      mensagem += "1. Gostaria de ver o nome dos projetos de lei\n"
      mensagem += "2. Gostaria de acessar o site da Câmara dos Deputados para mais detalhes?\n"
      return {"ok": True}
      

                                                                
                                                                
