from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.category import CategoryIn, CategoryPost, CategoryItemPost
from repository.purchase import PurchaseRepository
from repository.category import CategoryRepository
from .depends import get_category_repositories, get_token_repositories

route = APIRouter()

@route.post("/", status_code=200)
async def add_category(
    token: str,
    category_data: CategoryIn,
    category_repositories: CategoryRepository = Depends(get_category_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    category_data.token_sk = token_sk
    return await category_repositories.add_category(category_data)

@route.delete("/", status_code=204)
async def delete_category(
    token: str,
    category_data: CategoryItemPost,
    category_repositories: CategoryRepository = Depends(get_category_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):

    token_sk = await token_repositories.verify_access_token(token)
    category_data.token_sk = token_sk
    return await category_repositories.delete_category(category_data)

@route.get("/", status_code=200)
async def get_all(
    token: str,
    group_sk: str,
    customer_sk: str,
    category_repositories: CategoryRepository = Depends(get_category_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):

    token_sk = await token_repositories.verify_access_token(token)
    category_data = CategoryPost(
        token_sk=token_sk,
        customer_sk=customer_sk,
        group_sk=group_sk
    )
    return await category_repositories.get_all(category_data)

