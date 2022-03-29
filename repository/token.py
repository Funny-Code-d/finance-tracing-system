from .base import BaseRepository
from models.token import TokenIn

class TokenRepository(BaseRepository):
    
    async def create_token(self, u: TokenIn):
        """Создание токена для нового пользователя"""
        
        
    async def refresh_token(self):
        """Создание нового токена для существующего пользователя"""
        
    async def verify_token(self):
        """Проверка подлиности токена"""
        
    async def put_info_token(self):
        """Изменение информации о владельце токена"""
    
    async def delete_token(self):
        """Удаление токена"""
    
    
    
    
    async def generate_token() -> str:
        return 'generationg token'