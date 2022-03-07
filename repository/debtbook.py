from .base import BaseRepository


class DebtbookRepository(BaseRepository):
    
    async def create_debtbook(self):
        """Создание книжки"""
    
    async def delete_debtbook(self):
        """Удаление книжки"""
    
    async def add_debtor(self):
        """Добавление должника в книжку"""
    
    async def put_name_debtor(self):
        """Изменение имени должника в книжке"""
        
    async def get_all_info(self):
        """Получение всей информации из книжки (имя, сумма)"""
    
    async def get_history_by_id_debtor(self):
        """Получение истории изменения записи в книжке"""
    
    async def debt_additions(self):
        """Добавление долга"""
    
    async def debt_redemption(self):
        """Погашение долга"""
        
    async def binding_user_to_record_debtbook(self):
        """Привязка пользователя к записи в книжке"""