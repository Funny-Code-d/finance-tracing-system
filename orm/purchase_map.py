from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_purchase
from db.sattelites import sat_purchase, sat_purchase_detail
from db.links import link_purcahse_group, link_purchase_category
from models.purchase import PurchaseIn, Purchase
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime
class PurchaseEntity(BaseEntity):


    async def additing_purchase(self, purchase: Purchase):
        values = {
            "name_store" : purchase.name_store,
            "date_purchase" : datetime.now()
        }
        query = hub_purchase.insert().values(**values)
        purchase_sk = await self.database.execute(query=query)

        values = {
            "purchase_sk" : purchase_sk,
            "group_sk" : purchase.group_id
        }

        query = link_purcahse_group.insert().values(**values)
        await self.database.execute(query=query)

        values = {
            "purcahse_sk" : purchase_sk,
            "category_sk" : purchase.category_id
        }
        print(values)
        query = link_purchase_category.insert().values(**values)
        print(query)
        await self.database.execute(query=query)

        values = {
            "purchase_sk" : purchase_sk,
            "total_amount" : purchase.total_amount,
        }

        query = sat_purchase.insert().values(**values)
        await self.database.execute(query=query)

        for item in purchase.items:
            values = {
                "purchase_sk" : purchase_sk,
                "name_product" : item.name_product,
                "amount" : item.price,
                "quantity" : item.quantity
            }
            query = sat_purchase.insert().values(**values)
            await self.database.execute(query=query)
        
        return True
    

    async def delete_purchase(self, purchase_sk):
        query = link_purcahse_group.delete().where(
            link_purcahse_group.c.purchase_sk==purchase_sk
        )
        if await self.database.execute(query=query):
            query = sat_purchase_detail.delete().where(
                sat_purchase_detail.c.purchase_sk==purchase_sk
            )
            responce1_db = await self.database.execute(query=query)
            
            query = sat_purchase.delete().where(
                sat_purchase.c.purchase_sk==purchase_sk
            )
            responce2_db = await self.database.execute(query=query)

            if responce1_db and responce2_db:
                query = hub_purchase.delete().where(
                    hub_purchase.c.purchase_sk==purchase_sk
                )
                if await self.database.execute(query=query):
                    return True
                else:
                    return False
                
                

    async def get_by_date(self, date_start, date_end):
        query = select(
            sat_purchase.c.total_amount,
            sat_purchase.c.date_purchase,
            
        )

    async def get_by_category(self):
        pass

    async def get_by_date_and_category(self):
        pass