from src.models.user import (
    get_user_by_email
)


async def create_address(address_collection, users_collection, address, user_email):
    try:
        user = await get_user_by_email(users_collection, user_email)
        user_address = await get_address_by_user_id(address_collection, user["_id"])
        if user_address is None:
            address = await address_collection.insert_one({"user": user, "address": address})
            if address.inserted_id:
                address = await get_address(address_collection, address.inserted_id)
                return address
        else:
            address = await update_address(address_collection, user_address["_id"], address)
            if address.modified_count:
                return True, address.modified_count

            return False, 0
    except Exception as e:
        print(f'create_address.error: {e}')


async def update_address(address_collection, address_id, address_data):
    try:
        address = await address_collection.update_one(
            {'_id': address_id},
            {'$addToSet': {
                "address": address_data
            }}
        )

        return address
    except Exception as e:
        print(f'update_address.error: {e}')


async def get_address(address_collection, address_id):
    try:
        data = await address_collection.find_one({'_id': address_id})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')


async def get_address_by_user_id(address_collection, user_id):
    address = await address_collection.find_one({'user._id': user_id})
    return address


async def get_address_by_user_email(address_collection, user_email):
    address = await address_collection.find_one({'user.email': user_email})
    return address


async def delete_address(address_collection, address_id):
    try:
        address = await address_collection.delete_one(
            {'_id': address_id}
        )
        if address.deleted_count:
            return {'status': 'Address deleted'}
    except Exception as e:
        print(f'delete_address.error: {e}')
