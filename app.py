from flask import Flask, render_template, request
from api import addUser

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def initial():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass

    return render_template('Login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    print("Clicou cadastrar")

    
    return render_template('Cadastro.html')