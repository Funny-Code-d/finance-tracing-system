from pydantic import BaseModel
from typing import List, Optional
import datetime


class Category(BaseModel):
    category_sk: int
    name_category: str


class CategoryIn(BaseModel):
    customer_sk: int
    group_sk: str
    category_name: str


class PutCategory(CategoryIn):
    category_sk: int


class DeleteCategory(BaseModel):
    category_sk: int
    customer_sk: int
    group_sk: str