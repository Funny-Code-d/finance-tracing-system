from .base import BaseRepository


class PurchaseRepository(BaseRepository):
    
    
    async def add_purchase(self):
        """Добавление покупки"""
        
    async def delete_purchase(self):
        """Удаление покупки"""
    
    async def get_purchase_today(self):
        """Получение покупок за сегодня"""
        
    async def get_purchase_week(self):
        """Получение покупок за неделю"""
    
    async def get_purchase_month(self):
        """Получение покупок за месяц"""
        
    async def get_purchase_year(self):
        """Получение покупок за год"""
    
    async def get_purchase_date_range(self):
        """Получение покупок за выбранный период"""
    