from fastapi import APIRouter, Depends
from repository.group import GroupRepository
from repository.token import TokenRepository
from models.group import DeleteGroup, PostGroupModel, GetAllGroupModelRequest, GetGroupModelRequest, PatchGroupModel, \
    PutGroupModel
from .depends import get_group_repositories

route = APIRouter()


@route.post("/", status_code=204)
async def create_group(
        token: str,
        group: PostGroupModel,
        repositories: GroupRepository = Depends(get_group_repositories)):
    return await repositories.create_group(group=group, token=token)


@route.get("/all/")
async def get_all_group(
        token: str,
        user_id: int,
        repositories: GroupRepository = Depends(get_group_repositories)):
    return await repositories.get_list(user_id=user_id, token=token)


@route.get("/{group_id}")
async def get_by_id(
        token: str,
        group_id: str,
        repositories: GroupRepository = Depends(get_group_repositories)):
    return await repositories.get_by_id(group_id=group_id, token=token)


# @route.put("/", status_code=204)
# async def put(
#         token: str,
#         group: PutGroupModel,
#         repositories: GroupRepository = Depends(get_group_repositories)):
#     return await repositories.put(group=group)
#
#
# @route.patch("/", status_code=204)
# async def patch(
#         token: str,
#         group: PatchGroupModel,
#         repositories: GroupRepository = Depends(get_group_repositories),
#         token_repositories: TokenRepository = Depends(get_token_repositories)):
#     token_sk = await token_repositories.verify_access_token(token)
#     group.token_sk = token_sk
#     print(group)
#     return await repositories.patch(group=group)
#
#
# @route.delete("/", status_code=204)
# async def delete(
#         token: str,
#         group: DeleteGroup,
#         repositories: GroupRepository = Depends(get_group_repositories),
#         token_repositories: TokenRepository = Depends(get_token_repositories)):
#     token_sk = token_repositories.verify_access_token(token)
#     group.token_sk = token_sk
#     return await repositories.delete(group=group)
