from . import PRODUCTS
TABLES = [
    {
        'name': 'products',
        'schema': """CREATE TABLE products (
                        id INTEGER 
                        ,sku TEXT
                        ,description TEXT
                        ,category_name TEXT
                        ,initial_price FLOAT
                        ,sub_category_name TEXT
                        ,category_assistant TEXT)
                  """,
        'data': PRODUCTS.PRODUCTS,
    },
]
