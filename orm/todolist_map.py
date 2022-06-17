from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_todo_list
from db.settelites import set_item_todo_list
from db.links import link_group_todo_list, link_templates_category
from models.purchase import PurchaseIn, Purchase
from models.todolist import ToDoListIn
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime


class ToDoListEntity(BaseEntity):


    async def add_todolist(self, todolist_data: ToDoListIn):
        values = {
            "name_todo_list" : todolist_data.name_todolist,
            "is_active" : todolist_data.is_active
        }
        query = hub_todo_list.insert().values(**values)
        todolist_sk = await self.database.execute(query=query)

        
        values = {
            "todo_list_sk" : todolist_sk,
            "group_sk" : todolist_data.group_sk,
        }
        query = link_group_todo_list.insert().values(**values)
        await self.database.execute(query=query)

        for item in todolist_data.items:
            values = {
                "todo_list_sk" : todolist_sk,
                "name_item" : item.name_item,
                "price" : item.price,
                "quantity" : item.quantity,
                "complited" : item.complited
            }

            query = set_item_todo_list.insert().values(**values)
            await self.database.execute(query=query)
        
        return True
        
    

    async def delete_purchase(self, purchase_sk):
        pass
                
                

    async def get_by_date(self, date_start, date_end):
        query = select(
            set_purchase.c.total_amount,
            set_purchase.c.date_purchase,
            
        )

    async def get_by_category(self):
        pass

    async def get_by_date_and_category(self):
        pass