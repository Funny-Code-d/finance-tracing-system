from pydantic import BaseModel
from typing import List, Optional
import datetime


class ToDoListItem(BaseModel):
    todolist_item_sk: Optional[int]
    name_item: str
    price: float
    quantity: int
    # complited: bool

class ToDoList(BaseModel):
    todolist_sk: Optional[int]
    name_todolist: str
    is_active: bool
    items: List[ToDoListItem]

class ToDoListIn(ToDoList):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str

class ToDoListItemIn(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    todo_list_sk: int
    name_item: str
    price_item: float
    quantity_item: int

class GetToDoList(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str

class GetToDoListById(GetToDoList):
    todo_list_sk: Optional[int]


class DeleteToDoList(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    todo_list_sk: int

class DeleteItemToDoList(DeleteToDoList):
    item_todo_list_sk: int