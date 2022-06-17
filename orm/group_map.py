from sqlalchemy import select
from asyncpg.exceptions import UniqueViolationError
from .base import BaseEntity
from models.group import PostGroupModel, GetGroupModelRequest, GetAllGroupModelRequest, GroupModel
from models.group import GetGroupModelResponce, GetAllGroupModelResponce, PatchGroupModel
from db.hubs import hub_group, hub_customer
from db.settelites import set_group
from db.links import link_admin_group, link_token_customer
from pydantic.error_wrappers import ValidationError
from core.common_func import clear_dict

class GroupEntity(BaseEntity):

    


    async def add(self, group: PostGroupModel) -> int:

        group_sk = str(group.customer_sk) + str(group.name_group)
        values = {
            "group_sk" : group_sk,
            "access" : group.access
        }
        query = hub_group.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except UniqueViolationError:
            return None

        values = {
            "group_sk" : group_sk,
            "customer_sk" : group.customer_sk
        }
        query = link_admin_group.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except UniqueViolationError:
            return None
        

        values = {
            "group_sk" : group_sk,
            "name_group" : group.name_group,
            "description" : group.description
        }
        query = set_group.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except UniqueViolationError:
            return None

        return True

    async def get(self, group: GetGroupModelRequest) -> GetGroupModelResponce:
        
        query = select(
            hub_customer.c.customer_sk,
            hub_group.c.group_sk,
            hub_group.c.access,
            set_group.c.name_group,
            set_group.c.description
        )

        query = query.join_from(hub_customer, link_admin_group)
        query = query.join_from(link_admin_group, hub_group)
        query = query.join_from(hub_group, set_group)
        query = query.where(
            hub_group.c.group_sk==group.group_sk,
            hub_customer.c.customer_sk==group.customer_sk
        )

        try:
            return GetGroupModelResponce.parse_obj(await self.database.fetch_one(query=query))
        except ValidationError:
            return None
        

    async def getList(self, group: GetAllGroupModelRequest) -> GetAllGroupModelResponce:
        query = select(
            hub_customer.c.customer_sk,
            hub_group.c.group_sk,
            hub_group.c.access,
            set_group.c.name_group,
            set_group.c.description
        )

        query = query.join_from(hub_customer, link_admin_group)
        query = query.join_from(link_admin_group, hub_group)
        query = query.join_from(hub_group, set_group)
        query = query.where(
            hub_customer.c.customer_sk==group.customer_sk
        )

        responce_db = await self.database.fetch_all(query=query)

        if responce_db is not None:
            list_groups = list()
            for row in responce_db:
                list_groups.append(GroupModel.parse_obj(row))
            
            
            
            return GetAllGroupModelResponce(
                customer_sk=group.customer_sk,
                groups=list_groups
            )
        else:
            return None


    async def update(self, group: PatchGroupModel) -> bool:
        
        values = {
            "name_group" : group.group_name,
            "description" : group.description
        }
        values = clear_dict(target_dict=values, value=None)
        if len(values) > 0:
            query = set_group.update().values(**values).where(set_group.c.group_sk==group.group_sk)
            await self.database.execute(query=query)


    
        values = {
            "access" : group.access
        }

        if group.group_name is not None:
            values['group_sk'] = str(group.customer_sk) + str(group.group_name)

        values = clear_dict(target_dict=values, value=None)
        if len(values) > 0:
            query = hub_group.update().values(**values).where(hub_group.c.group_sk==group.group_sk)
            await self.database.execute(query=query)
    
        return True
        
    async def delete(self, group_sk: str):
        query = hub_group.delete().where(hub_group.c.group_sk==group_sk)
        await self.database.execute(query=query)
        return True