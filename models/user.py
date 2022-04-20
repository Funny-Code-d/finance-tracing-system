from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    customer_sk: Optional[int]
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: int
    
class UserRegistartion(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    telegram_id: Optional[int]
    password: str
    
class UserIn(BaseModel):
    user_id: Optional[int]
    email: Optional[EmailStr]
    telegram_id: Optional[int]

class HubCustomerModel(BaseModel):
    customer_sk: Optional[int]
    email: EmailStr
    telegram_id: int
    password: str

class SetCustomerModel(BaseModel):
    customer_sk: int
    first_name: str
    last_name: str

class LinkTokenCustomer(BaseModel):
    token_sk: int
    customer_sk: int
    
