from .base import BaseRepository
from orm.todolist_map import ToDoListEntity
from models.todolist import GetToDoList, ToDoListIn, ToDoListItemIn, GetToDoListById, DeleteToDoList, DeleteItemToDoList
from requests import post
from os import getenv


class TodoListRepositry(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: ToDoListEntity = orm_obj

    
    async def add_todo_list(self, todolist_data: ToDoListIn) -> bool:
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.add_todolist(todolist_data)
        else:
            return False
    
    async def add_item_todo_list(self, todolist_data: ToDoListItemIn) -> bool:
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.add_item_todolist(todolist_data)
        else:
            return False
        
    async def get_all(self, todolist_data: GetToDoList):
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.get_all(todolist_data)
        else:
            return False

    async def get_by_id(self, todolist_data: GetToDoListById):
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.get_by_id(todolist_data)
        else:
            return False
    
    async def delete_todo_list(self, todolist_data: DeleteToDoList):
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.delete_todo_list(todolist_data)
        else:
            return False

    async def delete_item_todo_list(self, todolist_data: DeleteItemToDoList):
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.delete_item_todo_list(todolist_data)
        else:
            return False
        
    async def complited_item(self, todolist_data: DeleteItemToDoList):
        if await self.db_orm.check(todolist_data.token_sk, todolist_data.customer_sk, todolist_data.group_sk):
            return await self.db_orm.complited_item(todolist_data)
        else:
            return False

