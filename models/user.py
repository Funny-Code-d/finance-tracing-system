from pydantic import BaseModel, EmailStr
from typing import Optional, List


class User(BaseModel):
    customer_sk: Optional[int]
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: int

    class Config:
        schema_extra = {
            "example" : {
                "customer_sk" : 1,
                "first_name" : "Example first name",
                "last_name" : "Example last name",
                "email" : "example@example.com",
                "telegram_id" : 1

            }
        }
class UserList(BaseModel):
    token_sk: Optional[int]
    users: List[User]
    
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
    
class UserPatch(BaseModel):
    customer_sk: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    telegram_id: Optional[int]

    class Config:
        schema_extra = {
            "example" : {
                "customer_sk" : 1,
                "first_name" : "first name (Optional)",
                "last_name" : "last name (Optional)",
                "email" : "example@example.com (Optional)",
                "telegram_id" : 1

            }
        }