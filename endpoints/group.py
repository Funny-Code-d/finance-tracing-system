from os import access
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.token import Token, TokenIn, TokenOut, TokenAuthIn
from .depends import get_token_repositories


route = APIRouter()

@route.post("/")
async def create_group():
    return "not working yet"

@route.get("/")
async def get_all_group():
    return "not working yet"


@route.get("/{group_id}")
async def get_by_id():
    return "not working yet"

@route.put("/")
async def partial_update():
    return "not working yet"

@route.patch("/")
async def full_update():
    return "not working yet"

