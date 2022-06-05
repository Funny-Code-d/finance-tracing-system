from fastapi import Response, status, HTTPException
from orm.group_map import GroupEntity
from models.group import PatchGroupModel, PostGroupModel, GetGroupModelRequest, GetAllGroupModelRequest, PutGroupModel, DeleteGroup

class GroupRepository():

    def __init__(self, orm_obj):
        self.db_orm: GroupEntity = orm_obj

    async def create_group(self, group: PostGroupModel):
        is_success = await self.db_orm.add(group=group)

        if is_success:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=status.HTTP_409_CONFLICT)


    async def get_by_id(self, group: GetGroupModelRequest):
        is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
        if is_valid:
            responce_db = await self.db_orm.get(group=group)
            if responce_db:
                return responce_db
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="nothing found")
        else:
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")

    async def get_list(self, group: GetAllGroupModelRequest):
        is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
        if is_valid:
            responce_db = await self.db_orm.getList(group=group)
            if responce_db:
                return responce_db
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="nothing found")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")
    
    async def put(self, group: PutGroupModel):
        is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
        if is_valid:
            responce_db = await self.db_orm.update(group=group)
            if responce_db:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return False
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")

    async def patch(self, group: PatchGroupModel):
        print(group.token_sk, group.customer_sk)
        is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
        print(is_valid)
        if is_valid:
            responce_db = await self.db_orm.update(group=group)
            if responce_db:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return False
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")


    async def delete(self, group: DeleteGroup):
        is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
        if is_valid:
            responce_db = await self.db_orm.delete(group.group_sk)
            if responce_db:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return False
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")