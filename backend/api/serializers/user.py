def DecodeUser(doc) -> dict:
    return {
        "_id": str(doc["_id"]),
        "email": doc["email"],
        "hash_password": doc["hash_password"]
    }

def DecodeUsers(docs) -> list:
    return [DecodeUser(doc) for doc in docs]