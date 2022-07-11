from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_category
from db.links import link_group_category
from models.purchase import PurchaseIn, Purchase
from models.category import Category, CategoryIn, CategoryOut, CategoryPost, CategoryItemPost, PutCategory
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime


class CategoryEntity(BaseEntity):


    async def add_category(self, category: CategoryIn):
        values = {
            "name_category" : category.category_name
        }
        query = hub_category.insert().values(**values)
        category_sk = await self.database.execute(query=query)

        values = {
            "category_sk" : category_sk,
            "group_sk" : category.group_sk
        }

        query = link_group_category.insert().values(**values)
        await self.database.execute(query=query)

        return True
    

    async def delete_category(self, category_data: CategoryItemPost):
        query = link_group_category.delete().where(
            link_group_category.c.category_sk==category_data.category_sk
        )
        await self.database.execute(query=query)

        query = hub_category.delete().where(
            hub_category.c.category_sk==category_data.category_sk
        )
        await self.database.execute(query=query)
        return True
                

    async def get_all(self, category_data: CategoryPost):
        query = select(
            hub_category.c.category_sk,
            hub_category.c.name_category
        ).join_from(link_group_category, hub_category).where(link_group_category.c.group_sk==category_data.group_sk)

        responce_db = await self.database.fetch_all(query=query)
        result = list()
        for row in responce_db:
            result.append(Category.parse_obj(row))
        # print(result)
        
        return CategoryOut(
            customer_sk=category_data.customer_sk,
            group_sk=category_data.group_sk,
            categories=result
        )

    async def put_category(self, category_data: PutCategory):
        
        values = {
            "name_category" : category_data.category_name
        }
        query = hub_category.update().values(**values).where(hub_category.c.category_sk==category_data.category_sk)

        await self.database.execute(query=query)

        return True