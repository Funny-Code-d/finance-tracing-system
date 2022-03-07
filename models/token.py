from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime


class Token(BaseModel):
    token_id: Optional[int]
    access_token: str
    refresh_token: str
    owner: str
    email: EmailStr
    application: str
    date_create: datetime.datetime
    date_end_token: datetime.datetime


class TokenIn(BaseModel):
    owner: str
    application: str
    
class TokenOut(BaseModel):
    owner: str
    email: EmailStr
    token: str
    date_end_token: datetime.datetime