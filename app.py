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

@app.route("/projetosaprovados")
def projetos():
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
        return df.to_html() # return a HTML representation of the dataframe
    else:
        return f"Error: {response.status_code}" # return an error message if the response was not successful
          

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message_text = update["message"]["text"]
    
    if message_text.lower() == '1':
        if dados['dados']:
            projetos_aprovados = []
            for projeto in dados['dados']:
                projetos_aprovados.append(f"{projeto['siglaTipo']} {projeto['numero']} - {projeto['ementa']}")
            bot.send_message(chat_id=chat_id, text="Projetos de Lei aprovados:\n" + "\n".join(projetos_aprovados))
        else:
            bot.send_message(chat_id=chat_id, text="Nenhum projeto de lei foi aprovado recentemente.")
    elif message_text.lower() == '2':
        bot.send_message(chat_id=chat_id, text="Acesse o site da Câmara dos Deputados para mais detalhes: https://www.camara.leg.br/busca-portal/projetoslegislativos/")
    else:
        mensagem = "Olá, aqui você tem acesso aos Projetos de Lei aprovados na Câmara dos Deputados. Escolha uma das opções abaixo:\n"
        mensagem += "1. Gostaria de ver o nome dos projetos de lei\n"
        mensagem += "2. Gostaria de acessar o site da Câmara dos Deputados para mais detalhes?\n"
        bot.send_message(chat_id=chat_id, text=mensagem)

    return "ok"
      


  
  



                                                                
                                                                
