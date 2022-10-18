from flask import Flask, redirect, render_template, request
from api import addAvaliacao, addUser, checkPassword, selectAllVisitas, selectUserByEmail
import pandas as pd

app = Flask(__name__)

user = {}

@app.route('/', methods=['POST', 'GET'])
def initial():
    if request.method == 'POST':
        email_login = request.form['email_login']
        senha_login = request.form['senha_login']

        userDB = selectUserByEmail(email_login)
        if userDB == []:
            return render_template('Login.html', error='Usuário não encontrado')
        else:
            if not checkPassword(senha_login, userDB[0].password):
                return render_template('Login.html', error='Senha inválida!')

            
            
            pk_userId = userDB[0].pk_userId
            username = userDB[0].username
            email = userDB[0].email
            password = userDB[0].password

            global user
            user = dict({'pk_userId':pk_userId, 'username':username, 'email':email, 'password':password})
            
            return redirect('homepage', code=303)


    return render_template('Login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    
    if request.method == 'POST':
        nome_cadastro = request.form['nome_cadastro']
        emailcadastro = request.form['emailcadastro']
        senha_cadastro = request.form['senha_cadastro']
        senhaconfirm_cadastro = request.form['senhaconfirm_cadastro']

        if senha_cadastro != senhaconfirm_cadastro:
            print("As senhas não conferem")
        else:
            addUser(nome_cadastro, emailcadastro, senha_cadastro)

    
    return render_template('Cadastro.html')

@app.route('/homepage', methods=['POST', 'GET'])
def homepage():
    global user
    
    if user == {}:
        return redirect('/')
    
    if request.method == 'POST':
        print(request.form['button_menu'])
        if request.form['button_menu'] == 'add_visita':
            pass
        elif request.form['button_menu'] == 'signout':
            user = {}
            return redirect('/')
        elif request.form['button_menu'] == 'submit':
            visita = request.form['select_visita']
            comentario = request.form['comentario']

            addAvaliacao(user['pk_userId'], visita, comentario)

    visitasDB = selectAllVisitas()
    visitas = []

    for visita in visitasDB:
        media = visita.media_score

        newAttr = ''
        
        if media == None:
            newAttr = 'NÃO HÁ'
        else:
            if media == 1:
                newAttr = 'TOTALMENTE POSITIVO'
            elif media == -1:
                newAttr = 'TOTALMENTE NEGATIVO'
            elif media == 0:
                newAttr = 'NEUTRO'
            elif media < 0:
                newAttr = 'PARCIALMENTE NEGATIVO'
            elif media > 0:
                newAttr = 'PARCIALMENTE POSITIVO'
        
        
        visitas.append({
            'id': visita.id,
            'professor': visita.professor,
            'descricao': visita.descricao,
            'qtd_avaliacoes': visita.qtd_avaliacoes,
            'media_score': visita.media_score,
            'media_str': newAttr
        })

    return render_template('Homescreen.html', visitas=visitas)

if __name__ == '__main__':
    print("Backend is running")
    
    app.run(debug=True)