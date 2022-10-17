from requests import session
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:R1Avvjp6nqy1@198.100.155.70:3306/sentimentos")

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    pk_userId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(length=50))
    email = sqlalchemy.Column(sqlalchemy.String(length=100))
    password = sqlalchemy.Column(sqlalchemy.String(length=200))

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def selectUserByEmail(email):
    employees = session.query(Users).filter_by(email=email).all()

    print(employees[0])
    
def addUser(username, email, password):
    password = password.encode('utf-8')
    
    cryptPassword = bcrypt.hashpw(password, bcrypt.gensalt())
    
    newUser = Users(username=username, email=email, password=cryptPassword)
    session.add(newUser)
    session.commit()