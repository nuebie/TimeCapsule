from fastapi import APIRouter, Depends, HTTPException, status
from schemas.token import Token, TokenData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.users import AuthenticateUser
from utils.token import encode_token

router = APIRouter(prefix="/login",
                   tags=['login'])


@router.post(path="/", response_model=Token)
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    #authenticate user
    is_authenticated = AuthenticateUser(user=request)
    if is_authenticated:
        access_token = encode_token(data={"sub": request.username})
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )