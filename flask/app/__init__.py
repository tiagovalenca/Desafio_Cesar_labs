from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Importando SQLAlchemy para o db
from flask_swagger_ui import get_swaggerui_blueprint

# Criando o App Flask
app = Flask(__name__)

# Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Tiago-Valenca-Desafio-Cesar-Labs"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

from app import views
from .model.product import Product
import os, csv

## Criando o Banco de dados de Produtos
db.create_all()

## Populando o banco de dados com os sapatos do arquivo shoes.csv
## Usando isto só pra fins do desafio, visto que não estou conectado a um banco de dados real
folder = os.path.dirname(os.path.abspath(__file__))
bd_csv = os.path.join(folder, 'shoes.csv')

with open(bd_csv, "r") as f:
    reader = csv.reader(f, delimiter=",")

    for line in list(reader)[1:]:
        product = Product(line[0],line[1],line[2],line[3])
        db.session.add(product)
        db.session.flush()
        db.session.commit()