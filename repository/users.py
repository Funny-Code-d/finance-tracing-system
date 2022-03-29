from .base import BaseRepository
from typing import List
from models.user import User, UserIn, UserRegistartion

class UserRepository(BaseRepository):
    
    async def get_all(self)-> List[User]:
        """Получение всех пользователей доступных по токену"""
    
    async def get_by_id(self, u: UserIn) -> User:
        """Получение пользователя по ID"""
        
    async def get_by_email(self, u: UserIn) -> User:
        """Получение пользователя по Email"""
    
    async def get_by_telegram_id(self, u: UserIn) -> User:
        """Получение пользовтеля по telegram_id"""
        
    async def create_user(self, u: UserRegistartion) -> User:
        """Создание пользователя"""
        
    async def put_user(self, u: User) -> User:
        """Изменение информации о пользователе"""
        
    async def delete_user(self, u: UserIn) -> User:
        """Удаление пользовтаеля"""
        
    async def merge_user_defferent_platform(self, u: UserIn) -> User:
        """Слияние учётных записей одного пользователя с разных платформ"""

