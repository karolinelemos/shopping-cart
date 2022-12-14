import asyncio

from src.controllers.users import users_crud
from src.controllers.address import address_crud
from src.controllers.products import products_crud
from src.controllers.carts import carts_crud

loop = asyncio.get_event_loop()
print('''
MENU:

[1] - Iniciar CRUD usuários
[2] - Iniciar CRUD endereço
[3] - Iniciar CRUD produtos
[4] - Iniciar CRUD carrinho
[5] - Sair
    ''')
option = int(input('Escolha uma opção: '))

while True:
    try:
        if (option == 1):
            op = users_crud
        elif (option == 2):
            op = address_crud
        elif (option == 3):
            op = products_crud
        elif (option == 4):
            op = carts_crud
        elif (option == 5):
            exit()
        else:
            print('Opção inválida')

        loop.run_until_complete(op())
    except (ValueError, TypeError) as error:
        print(error)
