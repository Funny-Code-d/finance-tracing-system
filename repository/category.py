from .base import BaseRepository
from orm.category_map import CategoryEntity
from models.purchase import ParsePay, PurchaseIn, PurchaseData, Purchase, PurchaseItem
from models.category import CategoryIn, CategoryPost, CategoryItemPost, PutCategory
from requests import post
from os import getenv


class CategoryRepository(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: CategoryEntity = orm_obj
        
        
    async def add_category(self, category_item: CategoryIn):
        if await self.db_orm.check(category_item.token_sk, category_item.customer_sk, category_item.group_sk):
            return await self.db_orm.add_category(category_item)
        else:
            return False
        
        

    async def delete_category(self, category_data: CategoryItemPost):
        if await self.db_orm.check(category_data.token_sk, category_data.customer_sk, category_data.group_sk):
            return await self.db_orm.delete_category(category_data)
        else:
            return False
        
        
    async def get_all(self, category_data: CategoryPost):
        if await self.db_orm.check(category_data.token_sk, category_data.customer_sk, category_data.group_sk):
            return await self.db_orm.get_all(category_data)
        else:
            return False
        
    
    async def put_category(self, category_data: PutCategory):
        if await self.db_orm.check(category_data.token_sk, category_data.customer_sk, category_data.group_sk):
            return await self.db_orm.put_category(category_data)
        else:
            return False

    