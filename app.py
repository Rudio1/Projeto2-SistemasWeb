from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def initial():
    response = requests.get('https://www.melivecode.com/api/users')

    usuarios = response.json()

    return render_template('Cadastro.html', usuarios=usuarios)