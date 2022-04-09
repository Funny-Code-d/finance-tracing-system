from lib2to3.pytree import Base
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime


class Token(BaseModel):
    token_id: Optional[int]
    access_token: str
    refresh_token: str
    owner: str
    email_owner: EmailStr
    date_create: datetime.datetime
    date_refresh: datetime.datetime
    # date_end: str


class TokenIn(BaseModel):
    owner: str
    email_owner: EmailStr
    password: str
    
class TokenOut(BaseModel):
    access_token: str
    refresh_token: str

class TokenAuthOut(BaseModel):
    access_token: str

class TokenAuthIn(BaseModel):
    refresh_token: str
    password: str