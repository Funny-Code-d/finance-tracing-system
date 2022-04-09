from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    user_id: Optional[int]
    token_id: int
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: int
    
class UserRegistartion(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    telegram_id: Optional[int]
    
class UserIn(BaseModel):
    user_id: Optional[int]
    email: Optional[EmailStr]
    telegram_id: Optional[int]
    
