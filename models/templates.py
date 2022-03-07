from pydantic import BaseModel
from typing import List
import datetime


class Category(BaseModel):
    category_id: int
    name_category: str


class RangeDate(BaseModel):
    date_start: datetime.datetime
    date_end: datetime.datetime


class Template(BaseModel):
    user_id: int
    template_id: int
    categories: List[Category]
    range_date: RangeDate
    
class DeleteTemplate(BaseModel):
    user_id: int
    template_id: int