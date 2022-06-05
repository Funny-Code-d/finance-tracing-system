from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_token
from db.settelites import set_token
from models.token import Token, TokenHash, TokenInfo
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List

class TokenEntity(BaseEntity):

    # Получение токенов (access в исходном состоянии, refresh захеширован)
    async def get_token(self, token_sk: int) -> TokenHash:
        query = select(
            hub_token.c.access_token,
            hub_token.c.refresh_token
        ).where(hub_token.c.token_sk==token_sk)
        
        try:
            return TokenHash.parse_obj(await self.database.fetch_one(query=query))
        except ValidationError:
            return None


    async def get_token_id(self, token:  str) -> int:
        query = hub_token.select().where(hub_token.c.access_token==token)
        try:
            responce_db = TokenHash.parse_obj(await self.database.fetch_one(query=query))
            return responce_db.token_sk
        except ValidationError:
            return None
        


    # Получение информации о токене
    async def get_token_info(self, token_sk: int) -> TokenInfo:
        query = select(
            set_token.c.name_owner,
            set_token.c.email_owner,
            set_token.c.date_create
        ).where(set_token.c.token_sk == token_sk)

        try:
            return TokenInfo.parse_obj(await self.database.fetch_one(query=query))
        except ValidationError:
            return None


    async def add(self, token: Token) -> int:
        values_hub_token = {
            "access_token" : token.access_token,
            "refresh_token" : token.refresh_token,
        }

        query = hub_token.insert().values(**values_hub_token)
        
        token_sk = await self.database.execute(query=query)
        
        values_set_token = {
            "token_sk" : token_sk,
            "name_owner" : token.owner,
            "email_owner" : token.email_owner,
            "date_create" : token.date_create
        }
        query = set_token.insert().values(**values_set_token)
        await self.database.execute(query=query)

        return token_sk


    async def update_access_token(self, token: TokenHash) -> None:
        values = {
            "access_token" : token.access_token
        }
        query = hub_token.update().where(hub_token.c.token_sk==token.token_sk).values(**values)
        await self.database.execute(query=query)
        return None

    async def delete(self, token_sk: int) -> None:

        query = set_token.delete().where(set_token.c.token_sk==token_sk)
        await self.database.execute(query=query)
        
        query = hub_token.delete().where(hub_token.c.token_sk==token_sk)
        await self.database.execute(query=query)
        return None