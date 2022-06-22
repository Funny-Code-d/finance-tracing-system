from .base import BaseRepository
from orm.templates_map import TemplatesEntity
from models.templates import GetGeneralStatistics, TemplatesIn, GetTemplates, DeleteTemplate, PatchTemplate
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
        
    async def patch_template(self, templates_data: PatchTemplate):
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            return await self.db_orm.patch_template(templates_data)
        else:
            return False
        
    
    async def get_general_statistics(self, templates_data: GetGeneralStatistics):
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            items = await self.db_orm.get_general_statistics(templates_data)
            if items:
                return {
                    "customer_sk" : templates_data.customer_sk,
                    "group_sk" : templates_data.group_sk,
                    "items" : items
                }
        else:
            return False
        
        
    async def get_general_statistics_detail(self, templates_data: GetGeneralStatistics):
        if await self.db_orm.check(templates_data.token_sk, templates_data.customer_sk, templates_data.group_sk):
            items = await self.db_orm.get_general_statistics_detail(templates_data)
            if items:
                return {
                    "customer_sk" : templates_data.customer_sk,
                    "group_sk" : templates_data.group_sk,
                    "items" : items
                }
        else:
            return False
    
    async def get_purchase_date_range(self):
        """Получение покупок за выбранный период"""
    