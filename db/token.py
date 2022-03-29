from .base import metadata, engine
import sqlalchemy
from models.token import TokenIn


async def insert_new_token(token_data: TokenIn):
    pass