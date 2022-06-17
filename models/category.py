from pydantic import BaseModel
from typing import List, Optional
import datetime


class Category(BaseModel):
    category_sk: int
    name_category: str

class CategoryOut(BaseModel):
    customer_sk: int
    group_sk: str
    categories: List[Category]

class CategoryIn(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    category_name: str

class CategoryPost(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str

class CategoryItemPost(CategoryPost):
    category_sk: int

