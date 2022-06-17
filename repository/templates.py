from .base import BaseRepository
from orm.templates_map import TemplatesEntity
from models.templates import TemplatesIn, GetTemplates, DeleteTemplate
from requests import post
from os import getenv


class TemplatesRepositry(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: TemplatesEntity = orm_obj

    
    async def add_template(self, templates_data: TemplatesIn) -> bool:
        """Добавление шаблона отчёта"""
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            return await self.db_orm.add_template(templates_data)
        else:
            return False


        
    async def get_all(self, templates_data: GetTemplates):
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            return await self.db_orm.get_all(templates_data)
        else:
            return False
    
    async def delete_template(self, templates_data: DeleteTemplate):
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            return await self.db_orm.delete_template(templates_data)
        else:
            return False
        
    async def get_purchase_week(self):
        """Получение покупок за неделю"""
    
    async def get_purchase_month(self):
        """Получение покупок за месяц"""
        
    async def get_purchase_year(self):
        """Получение покупок за год"""
    
    async def get_purchase_date_range(self):
        """Получение покупок за выбранный период"""
    