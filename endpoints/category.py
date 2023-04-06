from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.category import CategoryIn, DeleteCategory, PutCategory
from repository.category import CategoryRepository
from .depends import get_category_repositories

route = APIRouter()

@route.post("/", status_code=200)
async def add_category(
    token: str,
    data: CategoryIn,
    repository: CategoryRepository = Depends(get_category_repositories)):
    
    print(data.category_name)
    return await repository.create(
        name_category=data.category_name,
        customer_sk=data.customer_sk,
        group_sk=data.group_sk,
        token=token
        )


@route.get("/", status_code=200)
async def get_all(
    token: str,
    group_sk: str,
    customer_sk: str,
    category_repositories: CategoryRepository = Depends(get_category_repositories)):

    return await category_repositories.get_all(
        customer_sk=customer_sk,
        group_sk=group_sk,
        token=token
        )


@route.put("/", status_code=204)
async def change_category(
    token: str,
    data: PutCategory,
    category_repositories: CategoryRepository = Depends(get_category_repositories)):

    return await category_repositories.put_category(
        name_category=data.category_name,
        category_sk=data.category_sk,
        customer_sk=data.customer_sk,
        group_sk=data.group_sk,
        token=token
    )


@route.delete("/", status_code=204)
async def delete_category(
    token: str,
    data: DeleteCategory,
    category_repositories: CategoryRepository = Depends(get_category_repositories)):

    return await category_repositories.delete_category(
        category_sk=data.category_sk,
        customer_sk=data.customer_sk,
        group_sk=data.group_sk,
        token=token
    )
