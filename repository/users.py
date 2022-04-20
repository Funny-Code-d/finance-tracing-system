import email

from sqlalchemy import values
from sqlalchemy import select
from .base import BaseRepository
from typing import List
from models.user import User, UserIn, UserRegistartion, HubCustomerModel, SetCustomerModel, LinkTokenCustomer
from db.hubs import hub_token, hub_customer
from db.settelites import set_customer
from db.links import link_token_customer
from core import security

class UserRepository(BaseRepository):
    
    async def get_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        
        query = select([hub_token, link_token_customer, hub_customer]).where(link_token_customer.c.token_sk==hub_token.c.token_sk, link_token_customer.c.customer_sk==hub_customer.c.customer_sk)
        joined_tables = await self.database.fetch_all(query=query)
        for row in joined_tables:
            print(row.token_sk)
            print(row.access_token)
            print(row.customer_sk)
            print(row.email)
            print(row.teleram_id)
            print('-'*20)
        query = hub_customer.select().where(hub_customer.c.customer_sk==user_id)
        responce_hub_customer = await self.database.fetch_one(query=query)

        query = set_customer.select().where(set_customer.c.customer_sk==user_id)
        responce_set_customer = await self.database.fetch_one(query=query)
        
        if (responce_hub_customer is None) or (responce_set_customer is None):
            return False
        else:
            responce_hub_customer = HubCustomerModel.parse_obj(responce_hub_customer)
            responce_set_customer = SetCustomerModel.parse_obj(responce_set_customer)
            user = User(
                customer_sk=responce_hub_customer.customer_sk,
                first_name=responce_set_customer.first_name,
                last_name=responce_set_customer.last_name,
                email=responce_hub_customer.email,
                telegram_id=responce_hub_customer.telegram_id
            )
            return user
        
    async def get_by_email(self, email: str) -> User:
        """Получение пользователя по Email"""
        query = hub_customer.select().where(hub_customer.c.email==email)
        responce_hub_customer = await self.database.fetch_one(query=query)

        if responce_hub_customer is None:
            return False
        else:
            responce_hub_customer = HubCustomerModel.parse_obj(responce_hub_customer)
            print(responce_hub_customer)
            query = set_customer.select().where(set_customer.c.customer_sk==responce_hub_customer.customer_sk)
            responce_set_customer = SetCustomerModel.parse_obj(await self.database.fetch_one(query=query))
            user = User(
                customer_sk=responce_hub_customer.customer_sk,
                first_name=responce_set_customer.first_name,
                last_name=responce_set_customer.last_name,
                email=responce_hub_customer.email,
                telegram_id=responce_hub_customer.telegram_id
            )
            return user
    
    async def get_by_telegram_id(self, telegram_id: int) -> User:
        """Получение пользовтеля по telegram_id"""
        query = hub_customer.select().where(hub_customer.c.telegram_id==telegram_id)
        responce_db = await self.database.fetch_one(query=query)

        if responce_db is None:
            return False
        else:
            responce_hub_customer = HubCustomerModel.parse_obj(responce_db)
            query = set_customer.select().where(set_customer.c.customer_sk==responce_hub_customer.customer_sk)
            responce_set_customer = SetCustomerModel.parse_obj(await self.database.fetch_one(query=query))
            user = User(
                customer_sk=responce_hub_customer.customer_sk,
                first_name=responce_set_customer.first_name,
                last_name=responce_set_customer.last_name,
                email=responce_hub_customer.email,
                telegram_id=responce_hub_customer.telegram_id
            )
            return user
        
    async def create_user(self, u: UserRegistartion, token_id: int) -> User:
        """Создание пользователя"""        

        # Создание записи в hub_customer
        hub_customer_obj = HubCustomerModel(
            email=u.email,
            telegram_id=u.telegram_id,
            password=security.create_hash_token(u.email + u.password)
        )
        
        values = {**hub_customer_obj.dict()}
        values.pop("customer_sk", None)
        query = hub_customer.insert().values(**values)
        customer_sk = await self.database.execute(query=query)
        
        # Создание записи в set_customer
        set_customer_obj = SetCustomerModel(
            customer_sk=customer_sk,
            first_name=u.first_name,
            last_name=u.last_name
        )
        values = {**set_customer_obj.dict()}
        print(values)
        query = set_customer.insert().values(**values)
        await self.database.execute(query)
        
        # Создание записи в link_token_customer
        link_token_customer_obj = LinkTokenCustomer(
            token_sk=token_id,
            customer_sk=customer_sk
        )

        values = {**link_token_customer_obj.dict()}
        query = link_token_customer.insert().values(**values)
        await self.database.execute(query=query)
        
        return True

        
    async def put_user(self, u: User) -> User:
        """Изменение информации о пользователе"""
        
    async def delete_user(self, u: UserIn) -> User:
        """Удаление пользовтаеля"""
        
    async def merge_user_defferent_platform(self, u: UserIn) -> User:
        """Слияние учётных записей одного пользователя с разных платформ"""

