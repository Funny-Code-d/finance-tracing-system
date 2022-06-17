from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.token import Token, TokenIn, TokenOut, TokenAuthIn, TokenDelete
from models.purchase import PurchaseIn, DeletePurchase
from repository.purchase import PurchaseRepository
from .depends import get_purchase_repositories, get_token_repositories

route = APIRouter()

@route.post("/", status_code=200)
async def add_purchase(
    token: str,
    purchase_data: PurchaseIn,
    purchase_repositories: PurchaseRepository = Depends(get_purchase_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    purchase_data.token_sk = token_sk
    return await purchase_repositories.add_purchase(purchase_data=purchase_data)

@route.delete("/", status_code=204)
async def delete_purchase(
    token: str,
    purchase_data: DeletePurchase,
    purchase_repositories: PurchaseRepository = Depends(get_purchase_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    purchase_data.token_sk = token_sk
    
    return await purchase_repositories.delete_purchase(purchase_data=purchase_data)

