from flask import Flask, render_template, request
from api import addUser, checkPassword, selectUserByEmail

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def initial():
    if request.method == 'POST':
        email_login = request.form['email_login']
        senha_login = request.form['senha_login']

        user = selectUserByEmail(email_login)
        if user == []:
            return render_template('Login.html', error='Usuário não encontrado')
        else:
            print(senha_login)
            if not checkPassword(senha_login, user[0].password):
                return render_template('Login.html', error='Senha inválida!')
    elif request.method == 'GET':
        pass

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

if __name__ == '__main__':
    print("Backend is running")
    app.run(debug=True)