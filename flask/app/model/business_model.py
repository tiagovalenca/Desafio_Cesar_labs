from .product import Product
from flask import request
from .error_handler import InvalidUsage


# Classe Para Business Logic
class ProductBL:
    
    # Função Post
    # Recebe: um post request
    # Faz: verifica se todas as variáveis estão corretas, instancia um 
    #      produto com as variáveis recebidas e passa ele pra função create do produto
    # Retorna: o resultado da função create de produto
    def create(self, request):
        if request.form.get('brand') is None:
            raise InvalidUsage("There must be a Brand", status_code=410)
        brand = request.form.get('brand')

        if request.form.get('name') is None:
            raise InvalidUsage("There must be a Name", status_code=410)
        name = request.form.get('name')

        if isinstance(brand, str) is False:
            raise InvalidUsage("Brand is not str", status_code=410)
        if isinstance(name, str) is False:
            raise InvalidUsage("Name is not str", status_code=410)

        if request.form.get('price_on_sale') is None:
            raise InvalidUsage("There must be a price_on_sale", status_code=410)   
        try:
            price_on_sale = float(request.form.get('price_on_sale'))
        except ValueError:
            raise InvalidUsage("Price_on_sale is not a float", status_code=410)
        
        if request.form.get('full_price') is None:
            raise InvalidUsage("There must be a full_price", status_code=410)  
        try:
            full_price = float(request.form.get('full_price'))
        except ValueError:
            raise InvalidUsage("full_price is not a float", status_code=410)
        
        product = Product(brand, name, price_on_sale,full_price)

        return product.create()

    # Função Read
    # Recebe: um id ou nada
    # Faz: verifica se o id existe e se ele existir se é um int
    # Retorna: o resultado da função readTen ou o resultado da função read de Product
    def read(self, id=None):
        if not id:
            return Product.readTen()
        else:
            if isinstance(id, int) is False:
                raise InvalidUsage("id is not int", status_code=410)
            return Product.read(id)

    
    # Função Update
    # Recebe: um put request e um id
    # Faz: verifica se o id e os parâmetros recebidos estão corretos
    # Retorna: O resultado da função update de Product
    def update(self,request):

        if request.form.get('id') is None:
             raise InvalidUsage("Request has to have an id", status_code=410)
        
        brand = None
        name = None
        price_on_sale = None
        full_price = None

        try:
            id = int(request.form.get('id'))
        except ValueError:
            raise InvalidUsage("id is not int", status_code=410)

        if request.form.get('brand') is not None:
            brand = request.form.get('brand')
            if isinstance(brand, str)is False:
                raise InvalidUsage("Brand is not str", status_code=410)

        if request.form.get('name') is not None:
            name = request.form.get('name')
            if isinstance(name, str)is False:
                raise InvalidUsage("name is not str", status_code=410)

        if request.form.get('price_on_sale') is not None:
            try:
                price_on_sale = float(request.form.get('price_on_sale'))
            except ValueError:
                raise InvalidUsage("price_on_sale is not a float", status_code=410)

        if request.form.get('full_price') is not None:
            try:
                full_price = float(request.form.get('full_price'))
            except ValueError:
                raise InvalidUsage("full_price is not a float", status_code=410)

        return Product.update(id,brand,name,price_on_sale,full_price)


    # Função Delete
    # Recebe: um id
    # Faz: verifica se recebeu o id corretamente
    # Retorna: O resultado da função delete de Product
    def delete(self, id=None):
        if not id:
            raise InvalidUsage("Request has to have an id", status_code=410)

        return Product.delete(id)