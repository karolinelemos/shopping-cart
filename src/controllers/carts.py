from src.models.user import get_user_by_email
from src.models.carts import (
    add_product_cart,
    create_cart,
    delete_cart,
    delete_product_cart,
    get_cart_by_user_id
)
from src.server.database import connect_db, db, disconnect_db


async def carts_crud():
    print('''
    Carrinho:

    [1] - Criar carrinho
    [2] - Adicionar produto no carrinho
    [3] - Remover produto do carrtinho
    [4] - Ver total carrinho
    [5] - Remover carrinho
    ''')
    option = input("Entre com a opção de CRUD: ")

    await connect_db()
    carts_collection = db.order_collection
    users_collection = db.users_collection
    address_collection = db.address_collection
    products_collection = db.products_collection
    cart_item_collection = db.order_items_collection

    carrinho = {
        "price": 0,
        "paid": False,
    }
    user_email = 'teste@gmail.com'
    product_code = 97880

    if option == '1':
        # create cart
        cart = await create_cart(
            carts_collection,
            address_collection,
            users_collection,
            carrinho,
            user_email
        )
        print(cart)
    elif option == '2':
        # add product on cart
        address = await add_product_cart(
            cart_item_collection,
            users_collection,
            carts_collection,
            products_collection,
            user_email,
            product_code
        )
        print(address)
    elif option == '3':
        # delete product on cart
        result = await delete_product_cart(
            cart_item_collection,
            carts_collection,
            products_collection,
            users_collection,
            user_email,
            product_code
        )

        print(result)
    elif option == '4':
        # get total
        user = await get_user_by_email(
            users_collection,
            user_email
        )
        cart = await get_cart_by_user_id(carts_collection, user["_id"])
        print(f'Total: {cart["price"]}')
    elif option == '5':
        # delete cart
        user = await get_user_by_email(
            users_collection,
            user_email
        )
        cart = await get_cart_by_user_id(carts_collection, user["_id"])

        if cart is None:
            return print({'error': 'Cart not found'})

        result = await delete_cart(
            carts_collection,
            cart["_id"]
        )

        print(result)
    await disconnect_db()
