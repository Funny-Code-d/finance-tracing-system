from .base import BaseRepository


class UserRepository(BaseRepository):
    
    async def get_all(self):
        """Получение всех пользователей доступных по токену"""
    
    async def get_by_id(self):
        """Получение пользователя по ID"""
        
    async def get_by_email(self):
        """Получение пользователя по Email"""
    
    async def get_by_telegram_id(self):
        """Получение пользовтеля по telegram_id"""
        
    async def create_user(self):
        """Создание пользователя"""
        
    async def put_user(self):
        """Изменение информации о пользователе"""
        
    async def delete_user(self):
        """Удаление пользовтаеля"""
        
    async def merge_user_defferent_platform(self):
        """Слияние учётных записей одного пользователя с разных платформ"""
