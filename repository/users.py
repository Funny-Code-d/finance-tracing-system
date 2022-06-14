from fastapi import HTTPException, status
from sqlalchemy import select
from .base import BaseRepository
from orm.user_map import UserEntity
from typing import List
from models.user import User, UserIn, UserPatch, UserRegistartion, HubCustomerModel, SetCustomerModel, LinkTokenCustomer
from db.hubs import hub_token, hub_customer
from db.settelites import set_customer
from db.links import link_token_customer
from core import security
from pydantic.error_wrappers import ValidationError


class UserRepository():

    def __init__(self, orm_obj):
        self.db_orm: UserEntity = orm_obj
    
    async def get_all(self, token_id):
        return await self.db_orm.get_all(token_id)
        


    async def get_by_id(self, user_id: int, token_id: int) -> User:
        """Получение пользователя по ID"""

        user = await self.db_orm.get_by_id(user_id, token_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="nothing found")
        
        
    async def get_by_email(self, email: str, token_id: int) -> User:
        """Получение пользователя по Email"""
        
        user = await self.db_orm.get_by_email(email, token_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="nothing found")
    
    async def get_by_telegram_id(self, telegram_id: int, token_id: int) -> User:
        """Получение пользовтеля по telegram_id"""
        
        user = await self.db_orm.get_by_telegram(telegram_id, token_id)
        if user:
            return user
        else:
            return False
        
    async def create_user(self, u: UserRegistartion, token_id: int) -> User:
        """Создание пользователя"""        

        await self.db_orm.add(user=u, token_id=token_id)
        return True

        
    async def put_user(self, u: User, token_id: int) -> User:
        """Изменение информации о пользователе"""
        is_update = await self.db_orm.put(u)
        return is_update
    
    async def patch_user(self, u: UserPatch, token_id: int) -> User:
        """Изменение информации о пользователе"""
        is_update = await self.db_orm.patch(u)
        return is_update
        
    async def delete_user(self, u: UserIn) -> User:
        """Удаление пользовтаеля"""
        
    async def merge_user_defferent_platform(self, u: UserIn) -> User:
        """Слияние учётных записей одного пользователя с разных платформ"""

