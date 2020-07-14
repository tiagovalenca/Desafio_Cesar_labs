import json
from flask import request, jsonify, abort
from app import db, app
from .model.business_model import ProductBL
from .model.error_handler import InvalidUsage
from flask.views import MethodView
import os

# Mapeamento pra home page.
@app.route("/")
def index():

    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Olá avaliadores do Desafio Cesar Labs, estamos rodando o app em um container Docker utilizando Nginx!"

    return "Olá!"

# Criando a classe que vai ser o view do nosso Produto
# Ela vai conter o CRUD com nossos métodos, get, post, put, delete 
class ProductView(MethodView):
 
    # Função Get
    # Recebe: um id ou nada
    # Faz: verifica se o request recebido foi um get
    # Retorna: o resultado da função read do productbl
    def get(self, id=None):
        if request.method != 'GET':
            raise InvalidUsage('Method is not Get', status_code=400)
        
        if request.form.get('id') is not None:
            try:
                id = int(request.form.get('id'))
            except ValueError:
                raise InvalidUsage("id is not int", status_code=410)

        bl = ProductBL()
        return bl.read(id)
 
    # Função Post
    # Recebe: self
    # Faz: verifica se o request recebido é um post e passa ele pra função create do
    #       productbl
    # Retorna: o resultado da função create do productbl
    def post(self):
        if request.method != 'POST':
            raise InvalidUsage('Method is not Post', status_code=400)
        bl = ProductBL()
        return bl.create(request)
 
    # Função Put
    # Recebe: um request
    # Faz: verifica se o request recebido é um put e passa ele pra função update do
    #       ProductBL
    # Retorna: o resultado da função update do productbl
    def put(self):
        if request.method != 'PUT':
            raise InvalidUsage('Method is not Put', status_code=400)
        bl = ProductBL()
        return bl.update(request)
 
    # Função Delete
    # Recebe: um id
    # Faz: verifica se o request recebido é um delete e passa ele pra função delete do
    #       ProductBL
    # Retorna: o resultado da função delete do productbl
    def delete(self,id=None):
        if request.method != 'DELETE':
            raise InvalidUsage('Method is not Delete', status_code=400)

        if request.form.get('id') is not None:
            try:
                id = int(request.form.get('id'))
            except ValueError:
                raise InvalidUsage("id is not int", status_code=410)

        bl = ProductBL()
        return bl.delete(id)
 
 
product_view =  ProductView.as_view('product_view')

# Criando os Endpoints
app.add_url_rule(
    '/get/', view_func=product_view, methods=['GET']
)

app.add_url_rule(
    '/get/<int:id>', view_func=product_view, methods=['GET']
)
app.add_url_rule(
    '/post/', view_func=product_view, methods=['POST']
)

app.add_url_rule(
    '/put/', view_func=product_view, methods=['PUT']
)

app.add_url_rule(
    '/delete/', view_func=product_view, methods=['DELETE']
)

app.add_url_rule(
    '/delete/<int:id>', view_func=product_view, methods=['DELETE']
)