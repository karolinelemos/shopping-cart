# Cadastrar um produto, que possua nome, descrição, preço, e código
# identificador.
# Remover um produto pelo código.
from itertools import product


async def create_product(products_collection, product):
    try:
        product = await products_collection.insert_one(product)

        if product.inserted_id:
            product = await get_product(products_collection, product.inserted_id)
            return product

    except Exception as e:
        print(f'create_product.error: {e}')


async def get_product(products_collection, product_id):
    try:
        data = await products_collection.find_one({'_id': product_id})
        if data:
            return data
    except Exception as e:
        print(f'get_product.error: {e}')


async def get_product_by_code(products_collection, code):
    product = await products_collection.find_one({'code': code})
    return product


async def delete_product(products_collection, code):
    try:
        product = await products_collection.delete_one(
            {'code': code}
        )
        if product.deleted_count:
            return {'status': 'Product deleted'}
    except Exception as e:
        print(f'delete_product.error: {e}')
