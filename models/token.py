from lib2to3.pytree import Base
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime


class Token(BaseModel):
    token_id: Optional[int]
    access_token: Optional[str]
    refresh_token: Optional[str]
    owner: str
    email_owner: EmailStr
    date_create: datetime.datetime
    
class TokenIn(BaseModel):
    owner: str
    email_owner: EmailStr
    password: str
    
class TokenOut(BaseModel):
    token_sk: Optional[int]
    access_token: str
    refresh_token: str

class TokenAuthIn(BaseModel):
    access_token: str
    refresh_token: str
    password: str

class TokenDelete(BaseModel):
    access_token: str
    refresh_token: str

class TokenHash(BaseModel):
    token_sk: Optional[int]
    access_token: Optional[str]
    refresh_token: Optional[str]

class TokenInfo(BaseModel):
    name_owner: str
    email_owner: EmailStr
    date_create: datetime.datetime

