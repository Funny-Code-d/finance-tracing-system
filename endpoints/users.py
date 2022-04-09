from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repository.users import UserRepository
from repository.token import TokenRepository
from models.user import User, UserIn, UserRegistartion
from .depends import get_user_repository, get_token_repositories
# from .depends import get_current_user

route = APIRouter()




@route.post('/users')
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