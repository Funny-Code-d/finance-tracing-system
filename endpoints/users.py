from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repository.users import UserRepository
from repository.token import TokenRepository
from models.user import User, UserIn, UserRegistartion
from .depends import get_user_repository, get_token_repositories
# from .depends import get_current_user

route = APIRouter()




@route.post('/')
async def create_user(
    user: UserRegistartion,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_token(token)
    print(token_id)
    if token_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.create_user(u=user, token_id=token_id)


@route.get("/{user_id}")
async def get_by_id(
    user_id: int,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_token(token)
    print(token_id)
    if token_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_id(user_id=user_id)

@route.get("/by_email/{email}")
async def get_by_email(
    email: str,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_token(token)
    print(token_id)
    if token_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_email(email=email)

@route.get("/by_telegram_id/{telegram_id}")
async def get_by_telegram_id(
    telegram_id: int,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_token(token)
    print(token_id)
    if token_id is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_telegram_id(telegram_id=telegram_id)