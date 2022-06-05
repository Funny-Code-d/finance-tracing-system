from fastapi import APIRouter, Depends
from repository.group import GroupRepository
from repository.token import TokenRepository
from models.group import DeleteGroup, PostGroupModel, GetAllGroupModelRequest, GetGroupModelRequest, PatchGroupModel, PutGroupModel
from .depends import get_group_repositories, get_token_repositories


route = APIRouter()

@route.post("/", status_code=204)
async def create_group(
    token: str,
    group: PostGroupModel,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    token_sk = await token_repositories.verify_access_token(token)
    group.token_sk = token_sk

    return await repositories.create_group(group=group)


@route.get("/{customer_sk}")
async def get_all_group(
    token: str,
    customer_sk: int,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    
    token_sk = await token_repositories.verify_access_token(token)
    group = GetAllGroupModelRequest()
    group.customer_sk = customer_sk
    group.token_sk = token_sk
    return await repositories.get_list(group=group)


@route.get("/{customer_sk}/{group_id}")
async def get_by_id(
    token: str,
    customer_sk: int,
    group_id: str,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    

    token_sk = await token_repositories.verify_access_token(token)
    group = GetGroupModelRequest()
    group.customer_sk = customer_sk
    group.group_sk = group_id
    group.token_sk = token_sk
    return await repositories.get_by_id(group=group)
    

@route.put("/", status_code=204)
async def put(
    token: str,
    group: PutGroupModel,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    group.token_sk = token_sk
    return await repositories.put(group=group)

@route.patch("/", status_code=204)
async def patch(
    token: str,
    group: PatchGroupModel,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    group.token_sk = token_sk
    print(group)
    return await repositories.patch(group=group)

@route.delete("/", status_code=204)
async def delete(
    token: str,
    group: DeleteGroup,
    repositories: GroupRepository = Depends(get_group_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = token_repositories.verify_access_token(token)
    group.token_sk = token_sk
    return await repositories.delete(group=group)

