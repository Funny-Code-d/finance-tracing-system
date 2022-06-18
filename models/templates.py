from pydantic import BaseModel
from typing import List, Optional


class TemplatesCategory(BaseModel):
    category_sk: int
    name_category: str

class Templates(BaseModel):
    name_template: str
    number_days: int
    # categoties: List[TemplatesCategory]

class TemplatesIn(Templates):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    categories: List[int]

class TemplatesOutItem(Templates):
    categories: List[TemplatesCategory]

class TemplatesOut(BaseModel):
    # token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    items: List[TemplatesOutItem]

class GetTemplates(BaseModel):
    token_sk: int
    customer_sk: int
    group_sk: str

class DeleteTemplate(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    template_sk: int

class PatchTemplate(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    template_sk: int
    name_template: Optional[str]
    number_days: Optional[int]
    categories: Optional[List[int]]

