from sqlalchemy.orm import Session
from crud.users import read_user
from utils.password_hashing import verify_password

def AuthenticateUser(user):
    user_rec = read_user(user)
    if user:
        is_pword_verified = verify_password(plain_password=str(user.password), hashed_password=str(user_rec['hash_password']))
        if is_pword_verified:
            return True
        else:
            return False
    else:
        return False