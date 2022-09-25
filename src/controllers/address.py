from src.models.address import (
    create_address,
    get_address_by_user_email,
    delete_address,
)
from src.server.database import connect_db, db, disconnect_db


async def address_crud():
    print('''
    Endereços:

    [1] - Criar endereço
    [2] - Buscar endereço
    [3] - Deletar endereço
    ''')
    option = input("Entre com a opção de CRUD: ")

    await connect_db()
    address_collection = db.address_collection
    users_collection = db.users_collection

    address = [{
        "street": "Rua 1",
        "cep": "89555666",
        "district": "Bairro A",
        "city": "Cidade A",
        "state": "Estado B",
        "is_delivery": True,
    }]
    user_email = 'teste@gmail.com'

    if option == '1':
        # create address
        address = await create_address(
            address_collection,
            users_collection,
            address,
            user_email
        )
        print(address)
    elif option == '2':
        # get address
        address = await get_address_by_user_email(
            address_collection,
            user_email
        )
        print(address)
    elif option == '3':
        # delete
        address = await get_address_by_user_email(
            address_collection,
            user_email
        )

        result = await delete_address(
            address_collection,
            address["_id"]
        )

        print(result)

    await disconnect_db()
