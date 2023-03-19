def user_schema(user) -> dict:
    new_user = {**user, "id": str(user["_id"])}
    del new_user['_id']
    return new_user
