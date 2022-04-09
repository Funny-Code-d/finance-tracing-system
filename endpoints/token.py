from os import access
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.token import Token, TokenIn, TokenOut, TokenAuthIn
from .depends import get_token_repositories

route = APIRouter()

@route.post("/")
async def create_token(
    token: TokenIn,
    tokens: TokenRepository = Depends(get_token_repositories)):
    
    return await tokens.create_token(t=token)

@route.post("/refresh")
async def refresh_token(
    token: TokenAuthIn,
    tokens: TokenRepository = Depends(get_token_repositories)):
    
    responce = await tokens.refresh_token(token)

    if responce is False:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token did not pass the auth")
    else:
        return responce