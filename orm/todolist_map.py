from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_todo_list
from db.settelites import sat_item_todo_list
from db.links import link_group_todo_list, link_templates_category
from models.purchase import PurchaseIn, Purchase
from models.todolist import ToDoListIn, GetToDoList, GetToDoListById, ToDoListItemIn, DeleteToDoList, DeleteItemToDoList
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
                "complited" : False
            }

            query = sat_item_todo_list.insert().values(**values)
            await self.database.execute(query=query)
        
        return True

    async def add_item_todolist(self, todolist_data: ToDoListItemIn):

        values = {
            "todo_list_sk" : todolist_data.todo_list_sk,
            "name_item" : todolist_data.name_item,
            "price" : todolist_data.price_item,
            "quantity" : todolist_data.quantity_item,
            "complited" : False
        }
        
        query = sat_item_todo_list.insert().values(**values)
        await self.database.execute(query=query)
        return True
    

    async def get_all(self, todolist_data: GetToDoList):
        
        result = {
            "customer_sk" : todolist_data.customer_sk,
            "group_sk" : todolist_data.group_sk,
            "todolists" : list()
        }
        query = select(
            hub_todo_list.c.todo_list_sk,
            hub_todo_list.c.name_todo_list,
        ).join_from(link_group_todo_list, hub_todo_list).where(link_group_todo_list.c.group_sk==todolist_data.group_sk)

        responce_db = await self.database.fetch_all(query=query)
        for row in responce_db:

            item_todo_list = {
                "todo_list_sk" : row['todo_list_sk'],
                "name_todo_list" : row['name_todo_list'],
                "items" : list()
            }

            query = sat_item_todo_list.select().where(sat_item_todo_list.c.todo_list_sk==row['todo_list_sk'])

            item_todo_responce_db = await self.database.fetch_all(query=query)

            for item_todo_row in item_todo_responce_db:
                
                item_todo_list['items'].append({
                    "item_todo_list_sk" : item_todo_row['item_todo_list_sk'],
                    "name_item" : item_todo_row['name_item'],
                    "price" : item_todo_row['price'],
                    "quantity" : item_todo_row['quantity'],
                    "complited" : item_todo_row['complited']
                })
            result['todolists'].append(item_todo_list)

        return result
    
    async def get_by_id(self, todolist_data: GetToDoListById):

        result = {
            "customer_sk" : todolist_data.customer_sk,
            "group_sk" : todolist_data.group_sk,
            "todo_list_sk" : todolist_data.todo_list_sk,
            "items" : list()
        }

        query = sat_item_todo_list.select().where(sat_item_todo_list.c.todo_list_sk==todolist_data.todo_list_sk)
        responce_db = await self.database.fetch_all(query=query)

        for item_todo_row in responce_db:
                
            result['items'].append({
                "item_todo_list_sk" : item_todo_row['item_todo_list_sk'],
                "name_item" : item_todo_row['name_item'],
                "price" : item_todo_row['price'],
                "quantity" : item_todo_row['quantity'],
                "complited" : item_todo_row['complited']
            })
        
        return result

    
    async def delete_todo_list(self, todolist_data: DeleteToDoList):

        query = link_group_todo_list.delete().where(link_group_todo_list.c.todo_list_sk==todolist_data.todo_list_sk)

        await self.database.execute(query=query)

        query = hub_todo_list.delete().where(hub_todo_list.c.todo_list_sk==todolist_data.todo_list_sk)

        await self.database.execute(query=query)

        return True
    
    async def delete_item_todo_list(self, todolist_data: DeleteItemToDoList):

        query = sat_item_todo_list.delete().where(sat_item_todo_list.c.item_todo_list_sk==todolist_data.item_todo_list_sk)

        await self.database.execute(query=query)

        return True

    async def complited_item(self, todolist_data: DeleteItemToDoList):

        query = sat_item_todo_list.select().where(sat_item_todo_list.c.item_todo_list_sk==todolist_data.item_todo_list_sk)

        responce_db = await self.database.fetch_one(query=query)
    
        values = {
            "complited" : not responce_db['complited']
        }

        query = sat_item_todo_list.update().values(**values).where(sat_item_todo_list.c.item_todo_list_sk==todolist_data.item_todo_list_sk)

        await self.database.execute(query=query)

        return True