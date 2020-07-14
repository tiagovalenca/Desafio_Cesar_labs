from app import db
from flask import request, jsonify, abort
from .error_handler import InvalidUsage
 
 # Classe Produto, tem um id, uma marca, um nome, um preço quando em promoção e um preço sem promoção
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    name = db.Column(db.String(255))
    price_on_sale = db.Column(db.Float(asdecimal=True))
    full_price = db.Column(db.Float(asdecimal=True))

    # Função Init de Produto
    # Recebe: marca, nome, preço em promo e preço normal
    # Faz: cria um produto
    # Retorna: Nada
    def __init__(self, brand, name, price_on_sale, full_price):
        self.brand = brand
        self.name = name
        self.price_on_sale = price_on_sale
        self.full_price = full_price

    # Função Create
    # Recebe: um produto com brand, name, price_on_sale e full_price
    # Faz: cria o produto em nosso banco de dados
    # Retorna: o produto recebido em formato json
    def create(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

        return jsonify({self.id: {
            'brand': self.brand,
            'name': self.name,
            'price_on_sale': str(self.price_on_sale),
            'full_price': str(self.full_price)
        }})

    # Função read
    # Recebe: um id
    # Faz: Pega o produto do id recebido no banco de dados
    # Retorna: O produto em formato de json
    def read(id):
        product = Product.query.get(id)
        if not product:
            abort(404)
        result = {product.id: {
                   'brand': product.brand,
                   'name': product.name,
                    'price_on_sale': str(product.price_on_sale),
                    'full_price': str(product.full_price)
                }}
        return jsonify(result)

    # Função readTen
    # Recebe: nada
    # Faz: Pega os 10 primeiros produtos do banco de dados
    # Retorna: Os produtos em formato de json
    def readTen():
        products = Product.query.paginate(1, 10).items
        result = {}
        for product in products:
            result[product.id] = {
                'brand': product.brand,
                'name': product.name,
                'price_on_sale': str(product.price_on_sale),
                'full_price': str(product.full_price)
            }
            
        return jsonify(result)


    # Função Update
    # Recebe: id, e pode receber brand, name, price_on_sale, full_price
    # Faz: verifica se o id e os parâmetros recebidos estão corretos
    # Retorna: O produto atualizado em formato de json
    def update(id,brand=None,name=None,price_on_sale=None,full_price=None):
        product_to_update = Product.query.get(id)
        
        if not product_to_update:
            abort(404)
        
        if request.form.get('brand') is not None:
            product_to_update.brand = request.form.get('brand')

        if request.form.get('name') is not None:
            product_to_update.name = request.form.get('name')

        if request.form.get('price_on_sale') is not None:
            product_to_update.price_on_sale = request.form.get('price_on_sale')

        if request.form.get('full_price') is not None:
            product_to_update.full_price = request.form.get('full_price')

        db.session.flush()
        db.session.commit()
        return jsonify({product_to_update.id: {
            'brand': product_to_update.brand,
            'name': product_to_update.name,
            'price_on_sale': str(product_to_update.price_on_sale),
            'full_price': str(product_to_update.full_price)
        }})
 
    # Função Delete
    # Recebe: um id
    # Faz: deleta do banco de dados o produto que tem o id recebido
    # Retorna: Informação que o produto foi removido corretamente
    def delete(id):
        product = Product.query.get(id)
        if not product:
            abort(404)
        db.session.delete(product)
        db.session.flush()
        db.session.commit()
        return "Produto removido corretamente"