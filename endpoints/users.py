from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from repository.users import UserRepository
from repository.token import TokenRepository
from models.user import User, UserIn, UserRegistartion, UserPatch, UserAuth
from .depends import get_user_repository, get_token_repositories
# from .depends import get_current_user

route = APIRouter()




@route.post('/', status_code=204)
async def create_user(
    user: UserRegistartion,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    if token_id:
        if await users.create_user(u=user, token_id=token_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)


@route.get("/", status_code=200)
async def get_all(
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    # print(token)
    token_id = await verify_token.verify_access_token(token)
    if token_id:
        # print(token_id)
        return await users.get_all(token_id)


@route.get("/{user_id}")
async def get_by_id(
    user_id: int,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    print(token_id)
    if token_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_id(user_id=user_id, token_id=token_id)

@route.get("/by_email/{email}", response_model=User)
async def get_by_email(
    email: str,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    print(token_id)
    if token_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_email(email=email, token_id=token_id)

@route.get("/by_telegram_id/{telegram_id}", response_model=User)
async def get_by_telegram_id(
    telegram_id: int,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    print(token_id)
    if token_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        return await users.get_by_telegram_id(telegram_id=telegram_id, token_id=token_id)

@route.put("/", status_code=204)
async def put_user(
    user: User,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    if token_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        await users.put_user(u=user, token_id=token_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)



@route.patch("/", status_code=204)
async def patch_user(
    user: UserPatch,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    if token_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")
    else:
        await users.patch_user(u=user, token_id=token_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@route.post("/auth", status_code=200)
async def auth_user(
    user: UserAuth,
    token: str,
    users: UserRepository = Depends(get_user_repository),
    verify_token: TokenRepository = Depends(get_token_repositories)):

    token_id = await verify_token.verify_access_token(token)
    user.token_sk = token_id
    return await users.auth(user)