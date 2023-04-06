from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
   return "Olá, mundo!"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"
