from flask import Flask, redirect, render_template, request
from api import addAvaliacao, addUser, checkPassword, selectAllVisitas, selectUserByEmail

app = Flask(__name__)

visitas = []
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
    if user == {}:
        return redirect('/')
    
    if request.method == 'POST':

        visita = request.form['select_visita']
        comentario = request.form['comentario']

        addAvaliacao(user['pk_userId'], visita, comentario)
        pass

    global visitas
    visitas = selectAllVisitas()
    
    return render_template('Homescreen.html', visitas=visitas)

if __name__ == '__main__':
    print("Backend is running")
    
    app.run(debug=True)