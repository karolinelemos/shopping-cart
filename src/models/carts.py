from src.models.products import (
    get_product_by_code
)
from src.models.address import (
    get_available_address
)
from src.models.user import (
    get_user_by_email
)


async def create_cart(carts_collection, address_collection, users_collection, cart, user_email):
    try:
        user = await get_user_by_email(users_collection, user_email)
        user_address = await get_available_address(address_collection, user_email)
        user_cart = await get_cart_by_user_id(carts_collection, user["_id"])

        cart = {
            "user": user["_id"],
            "price": cart["price"],
            "paid": cart["paid"],
            "address": user_address["_id"]
        }

        if user_cart is None:
            cart = await carts_collection.insert_one(cart)
            if cart.inserted_id:
                cart = await get_cart(carts_collection, cart.inserted_id)
                return cart
        else:
            return False, 0
    except Exception as e:
        print(f'create_address.error: {e}')


async def get_cart(carts_collection, cart_id):
    try:
        data = await carts_collection.find_one({'_id': cart_id})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')


async def get_cart_by_user_id(carts_collection, user_id):
    cart = await carts_collection.find_one({'user': user_id})
    return cart


async def add_product_cart(cart_item_collection, users_collection, carts_collection, products_collection, user_email, product_code):
    user = await get_user_by_email(users_collection, user_email)
    cart = await get_cart_by_user_id(carts_collection, user["_id"])
    product = await get_product_by_code(products_collection, product_code)

    item = await cart_item_collection.insert_one({"order": cart["_id"], "product": product})
    if item.inserted_id:
        new_price = cart["price"] + product["price"]
        await update_cart(carts_collection, cart["_id"], {"price": new_price})


async def update_cart(carts_collection, cart_id, data):
    try:
        cart = await carts_collection.update_one(
            {'_id': cart_id},
            {'$set': data}
        )

        if cart.modified_count:
            return True, cart.modified_count

        return False, 0
    except Exception as e:
        print(f'update_user.error: {e}')


async def get_item(cart_item_collection, item_id):
    try:
        data = await cart_item_collection.find_one({'_id': item_id})
        if data:
            return data
    except Exception as e:
        print(f'get_item.error: {e}')


async def delete_product_cart(carts_item_collection, carts_collection, products_collection, users_collection, user_email, product_code):
    try:
        user = await get_user_by_email(users_collection, user_email)
        cart = await get_cart_by_user_id(carts_collection, user["_id"])
        product = await get_product_by_code(products_collection, product_code)

        item = await carts_item_collection.delete_one(
            {'product.code': product_code, "order": cart["_id"]}
        )
        if item.deleted_count:
            new_price = cart["price"] - product["price"]
            await update_cart(carts_collection, cart["_id"], {"price": new_price})
            return {'status': 'Item deleted'}
    except Exception as e:
        print(f'delete_address.error: {e}')


async def delete_cart(carts_collection, cart_id):
    try:
        cart = await carts_collection.delete_one(
            {'_id': cart_id}
        )

        if cart.deleted_count:
            return {'status': 'Cart deleted'}
    except Exception as e:
        print(f'delete_cart.error: {e}')
