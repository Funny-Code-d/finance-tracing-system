from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from repository.users import UserRepository
from repository.token import TokenRepository
from models.user import User, UserIn, UserRegistartion, UserPatch, UserAuth, DeleteUser
from .depends import get_user_repositories

# from .depends import get_current_user

route = APIRouter()


@route.post('/', status_code=200)
async def create_user(
        user: UserRegistartion,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.create_user(user, token=token)


@route.get("/", status_code=200)
async def get_all(
        token: str,
        repository: UserRepository = Depends(get_user_repositories),):
    return await repository.get_all(token=token)


@route.get("/{user_id}")
async def get_by_id(
        user_id: int,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.get_by_id(user_id, token=token)


@route.get("/email/{email}", response_model=User)
async def get_by_email(
        email: str,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.get_by_email(email, token=token)


@route.get("/telegram/{telegram_id}", response_model=User)
async def get_by_telegram_id(
        telegram_id: int,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.get_by_telegram(telegram_id, token=token)


@route.put("/", status_code=204)
async def put_user(
        user: User,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.put_user(user, token=token)


@route.patch("/", status_code=204)
async def patch_user(
        user: UserPatch,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.patch_user(user, token=token)


@route.post("/auth", status_code=200)
async def auth_user(
        user: UserAuth,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.get_all(user, token=token)


@route.delete("/", status_code=204)
async def delete_user(
        user: DeleteUser,
        token: str,
        repository: UserRepository = Depends(get_user_repositories)):
    return await repository.delete_user(user, token=token)
