from db.db_conn import users_collection
from serializers.user import DecodeUser

def read_user(user):
    query = {"email": user.username}
    resp = users_collection.find_one(query)
    decoded_data = DecodeUser(resp)
    return decoded_data