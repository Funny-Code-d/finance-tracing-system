from .base import BaseRepository


class TemplatesRepository(BaseRepository):
    
    async def get_all(self):
        """Получение всех шаблонов (описание шаблонов)"""
    
    async def get_purchase_by_template_id(self):
        """Получение покупок по выбранному шаблону"""
        
    async def create_template(self):
        """Создание шаблона"""
    
    async def delete_template(self):
        """Удаление шаблона"""
    
    async def put_template(self):
        """Изменение шаблона"""