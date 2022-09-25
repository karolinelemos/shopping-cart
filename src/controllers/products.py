# Cadastrar um produto, que possua nome, descrição, preço, e código e identificador.
# Remover um produto pelo código.
from src.models.products import (
    create_product,
    delete_product,
    get_product_by_code
)
from src.server.database import connect_db, db, disconnect_db


async def products_crud():
    print('''
    Endereços:

    [1] - Cadastrar produto
    [2] - Remover produto
    ''')
    option = input("Entre com a opção de CRUD: ")

    await connect_db()
    products_collection = db.products_collection

    product = {
        "name": "Bicicleta Aro 29 Freio a Disco 21M. Velox Branca/Verde - Ello Bike",
        "description": "Bicicleta produzida com materiais de qualidade e foi criada pensando nas pessoas que desejam praticar o ciclismo e ter uma vida saudável sem abrir mão de conforto um excelente custo x benefício.",
        "price": 898.2,
        "code": 97880
    }

    if option == '1':
        # create product
        product = await create_product(
            products_collection,
            product
        )
        print(product)
    elif option == '2':
        # delete
        product = await get_product_by_code(
            products_collection,
            product["code"]
        )

        result = await delete_product(
            products_collection,
            product["code"]
        )

        print(result)

    await disconnect_db()
