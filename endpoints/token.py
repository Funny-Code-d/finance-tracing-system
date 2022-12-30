from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.token import Token, TokenIn, TokenOut, TokenAuthIn, TokenDelete
from .depends import get_token_repositories

route = APIRouter()


@route.post("/", status_code=200)
async def create_token(token: TokenIn, tokens: TokenRepository = Depends(get_token_repositories)):
    return await tokens.create_token(token)


@route.post("/refresh", status_code=200)
async def refresh_token(token: TokenAuthIn, tokens: TokenRepository = Depends(get_token_repositories)):
    
    return await tokens.refresh_token(token)


@route.delete("/", status_code=204)
async def delete_token(token: TokenDelete, tokens: TokenRepository = Depends(get_token_repositories)):

    return await tokens.delete_token(token)
