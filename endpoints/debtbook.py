from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.debtbook import DebtbookIn, PostTransaction
from repository.purchase import PurchaseRepository
from repository.debtbook import DebtorRepository
from .depends import get_debtbook_repositories, get_token_repositories

route = APIRouter()

@route.post("/", status_code=200)
async def add_debtor(
    token: str,
    debtor_data: DebtbookIn,
    debtor_repositories: DebtorRepository = Depends(get_debtbook_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    debtor_data.token_sk = token_sk
    return await debtor_repositories.add_debtor(debtor_data)

@route.get("/{customer_sk}", status_code=200)
async def get_all_debtbook_record(
    token: str,
    customer_sk: int,
    debtor_repositories: DebtorRepository = Depends(get_debtbook_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    return await debtor_repositories.get_all(token_sk=token_sk, customer_sk=customer_sk)


@route.post("/regist", status_code=200)
async def regist_transaction(
    token: str,
    debt_data: PostTransaction,
    debtor_repositories: DebtorRepository = Depends(get_debtbook_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    debt_data.token_sk = token_sk
    return await debtor_repositories.regist_transaction(debt_data)
