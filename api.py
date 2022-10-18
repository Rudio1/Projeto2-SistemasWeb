from requests import session
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import json
import requests
import base64
import pprint

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:R1Avvjp6nqy1@198.100.155.70:3306/sentimentos")

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    pk_userId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(length=50))
    email = sqlalchemy.Column(sqlalchemy.String(length=100))
    password = sqlalchemy.Column(sqlalchemy.String(length=200))

class Visitas(Base):
    __tablename__ = 'visitas'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    professor = sqlalchemy.Column(sqlalchemy.String(length=100))
    descricao = sqlalchemy.Column(sqlalchemy.String(length=50))

class Avaliacoes(Base):
    __tablename__ = 'avaliacoes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Users.pk_userId))
    visita = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Visitas.id))
    data = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    avaliacao = sqlalchemy.Column(sqlalchemy.String(200))
    score = sqlalchemy.Column(sqlalchemy.FLOAT)
    label = sqlalchemy.Column(sqlalchemy.String(50))

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def selectUserByEmail(email):
    user = session.query(Users).filter_by(email=email).all()

    return user
    
def addUser(username, email, password):
    password = password.encode('utf-8')
    
    cryptPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
    
    newUser = Users(username=username, email=email, password=cryptPassword)
    session.add(newUser)
    session.commit()

def getSentimento(mensagem):
    url = 'https://api.gotit.ai/NLU/v1.5/Analyze'
    data = {"T":""+mensagem+"","S": True}

    data_json = json.dumps(data)
    userAndPass = base64.b64encode(b"2535-gW2JabDc:C9TWur+KD9WLTEcwqu9LWye0TBnL+Cr/YdX5aX5e").decode("ascii")
    headers = {'Content-type': 'application/json', "Authorization": "Basic %s" %  userAndPass}
    response = requests.post(url, data=data_json, headers=headers)
    return response.json()['sentiment']

def addAvaliacao(user, visita, avaliacao):
    sentimento = getSentimento(avaliacao)
    
    newAvaliacao = Avaliacoes(user=user, visita=visita, avaliacao=avaliacao, score=sentimento['score'], label=sentimento['label'])
    session.add(newAvaliacao)
    session.commit()

def selectAllVisitas():
    return engine.engine.execute('SELECT *, (SELECT COUNT(b.score) FROM avaliacoes b WHERE a.id=b.visita) AS qtd_avaliacoes, (SELECT AVG(b.score) FROM avaliacoes b WHERE a.id=b.visita) AS media_score FROM visitas a')

def checkPassword(password, hashed):
    password = password.encode('utf-8')

    return bcrypt.checkpw(password, hashed.encode('utf-8'))