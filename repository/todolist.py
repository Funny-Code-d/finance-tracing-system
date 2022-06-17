from .base import BaseRepository
from orm.todolist_map import ToDoListEntity
from models.templates import TemplatesIn
from requests import post
from os import getenv


class TodoListRepositry(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: ToDoListEntity = orm_obj

    
    async def add_template(self, todolist_data: TemplatesIn) -> bool:
        """Добавление шаблона отчёта"""
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.add_todolist(todolist_data)
        else:
            return False


        
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
    