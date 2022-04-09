import email
from .base import BaseRepository
from typing import List
from models.user import User, UserIn, UserRegistartion
from db.token import token_table
from db.customer import customers


class UserRepository(BaseRepository):
    
    async def get_all(self)-> List[User]:
        """Получение всех пользователей доступных по токену"""
    
    async def get_by_id(self, u: UserIn) -> User:
        """Получение пользователя по ID"""
        
    async def get_by_email(self, u: UserIn) -> User:
        """Получение пользователя по Email"""
    
    async def get_by_telegram_id(self, u: UserIn) -> User:
        """Получение пользовтеля по telegram_id"""
        
    async def create_user(self, u: UserRegistartion, token_id: int) -> User:
        """Создание пользователя"""        
        user = User(
            token_id=token_id,
            first_name=u.first_name,
            last_name=u.last_name,
            telegram_id=u.telegram_id,
            email=u.email
        )
        values = {**user.dict()}
        values.pop('user_id', None)
        print(values)
        query = customers.insert().values(**values)
        user.user_id = await self.database.execute(query)
        return user

        
    async def put_user(self, u: User) -> User:
        """Изменение информации о пользователе"""
        
    async def delete_user(self, u: UserIn) -> User:
        """Удаление пользовтаеля"""
        
    async def merge_user_defferent_platform(self, u: UserIn) -> User:
        """Слияние учётных записей одного пользователя с разных платформ"""

