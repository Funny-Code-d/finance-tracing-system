from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    user_id: Optional[int]
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: int
    
class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    telegram_id: Optional[int]
