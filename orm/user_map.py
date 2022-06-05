from pydantic.error_wrappers import ValidationError
from .base import BaseEntity
from sqlalchemy import select
from core.common_func import clear_dict
from db.hubs import hub_token, hub_customer
from db.links import link_token_customer
from db.settelites import set_customer

from models.user import User, UserList, UserPatch, UserRegistartion
from models.user import HubCustomerModel, SetCustomerModel

class UserEntity(BaseEntity):

    def generate_select_join(self):
        query = select(
            hub_customer.c.customer_sk,
            hub_customer.c.email,
            hub_customer.c.telegram_id,
            set_customer.c.first_name,
            set_customer.c.last_name
        )
        query = query.join_from(hub_token, link_token_customer)
        query = query.join_from(link_token_customer, hub_customer)
        query = query.join_from(hub_customer, set_customer)

        return query
    
    def clean_model_data(self, target_dict):
        result = dict()
        for key in target_dict.keys():
            if target_dict[key] != None:
                result[key] = target_dict[key]
        return result


    async def get_by_id(self, user_id: int, token_id: int) -> User:
        query = self.generate_select_join()
        query = query.where(
            hub_customer.c.customer_sk==user_id,
            hub_token.c.token_sk==token_id
        )
        try:
            responce_db = await self.database.fetch_one(query=query)
            if responce_db:
                return User.parse_obj(responce_db)
            else:
                return None
        except ValidationError:
            return False


    async def getList(self, token_id: int) -> UserList:

        query = self.generate_select_join()
        query = query.where(
            hub_token.c.token_sk==token_id
        )

        response_db = await self.database.fetch_all(query=query)

        users = {
            "token_sk" : token_id,
            "users" : response_db
        }

        try:
            return UserList.parse_obj(users)
        except ValidationError:
            return False


    async def get_by_email(self, email: str, token_id: int) -> User:

        query = self.generate_select_join()
        query = query.where(
            hub_customer.c.email==email,
            hub_token.c.token_sk==token_id
        )
        print(query)
        try:
            # return User.parse_obj(await self.database.fetch_one(query=query))
            responce_db = await self.database.fetch_one(query=query)
            if responce_db:
                return User.parse_obj(responce_db)
            else:
                return None
        except ValidationError:
            return False

    async def get_by_telegram(self, telegram_id: int, token_id: int) -> User:

        query = self.generate_select_join()
        query = query.where(
            hub_customer.c.telegram_id==telegram_id,
            hub_token.c.token_sk==token_id
        )

        try:
            responce_db = await self.database.fetch_one(query=query)
            if responce_db:
                return User.parse_obj(responce_db)
            else:
                return None
        except ValidationError:
            return False

    async def add(self, user: UserRegistartion, token_id: int):
        # create record in hub_customer
        values_hub = {
            "email" : user.email,
            "telegram_id" : user.telegram_id,
            "password" : user.password
        }

        query = hub_customer.insert().values(**values_hub)
        user_sk = await self.database.execute(query=query)

        # create record in set_customer
        values_set = {
            "customer_sk" : user_sk,
            "first_name" : user.first_name,
            "last_name" : user.last_name
        }

        query = set_customer.insert().values(**values_set)
        await self.database.execute(query=query)

        # create record in link_token_customer
        values_link = {
            "customer_sk" : user_sk,
            "token_sk" : token_id
        }
        query = link_token_customer.insert().values(**values_link)
        await self.database.execute(query=query)

        return True


    async def put(self, user: User):
        values_hub = {
            "email" : user.email,
            "telegram_id" : user.telegram_id
        }

        values_set = {
            "first_name" : user.first_name,
            "last_name" : user.last_name
        }

        query = hub_customer.update().values(**values_hub).where(hub_customer.c.customer_sk == user.customer_sk)
        await self.database.execute(query=query)

        query  = set_customer.update().values(**values_set).where(hub_customer.c.customer_sk == user.customer_sk)
        await self.database.execute(query=query)
    
    async def patch(self, user: UserPatch) -> bool:
        was_updated = False
        values_hub = {
            "email" : user.email,
            "telegram_id" : user.telegram_id
        }

        values_set = {
            "first_name" : user.first_name,
            "last_name" : user.last_name
        }

        values_hub = clear_dict(values_hub, None)
        values_set = clear_dict(values_set, None)

        if len(values_hub) > 0:
            query = hub_customer.update().values(**values_hub).where(hub_customer.c.customer_sk==user.customer_sk)
            await self.database.execute(query=query)
            was_updated = True
        
        if len(values_set) > 0:
            query = set_customer.update().values(**values_set).where(set_customer.c.customer_sk==user.customer_sk)
            await self.database.execute(query=query)
            was_updated = True
        
        return was_updated


    async def delete(self, user_id: int, token_id: int):
        query = link_token_customer.select().where(
            link_token_customer.c.customer_sk==user_id,
            link_token_customer.c.token_sk==token_id
        )

        is_existence = await self.database.fetch_one(query=query)

        if is_existence is not None:
            query = link_token_customer.delete().where(
                link_token_customer.c.customer_sk==user_id,
                link_token_customer.c.token_sk==token_id
            )
            self.database.execute(query=query)

            query = hub_customer.delete().where(
                hub_customer.c.customer_sk==user_id
            )
            self.database.execute(query=query)

            query = set_customer.delete().where(
                set_customer.c.customer_sk==user_id
            )
            self.database.execute(query=query)
        else:
            return False