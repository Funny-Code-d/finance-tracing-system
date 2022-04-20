from typing import List

from fastapi import HTTPException, status
from .base import BaseRepository
from models.token import TokenIn, Token, TokenOut, TokenAuthOut, TokenAuthIn, HubTokenModel, SetTokenModel
from db.hubs import hub_token
from db.settelites import set_token
from core import security
import datetime

class TokenRepository(BaseRepository):
    

    async def create_token(self, t: TokenIn) -> TokenOut:
        """Создание токена для нового пользователя"""

        access_token = security.create_hash_token(t.owner + t.email_owner)
        refresh_token = security.create_hash_token(t.owner + t.email_owner + t.password)

        token = HubTokenModel(
            access_token=access_token,
            refresh_token=security.create_hash_token(refresh_token)
        )
        values = {**token.dict()}
        values.pop("token_sk", None)
        
        query = hub_token.insert().values(**values)
        token_sk = await self.database.execute(query)
        
        token = SetTokenModel(
            token_sk=token_sk,
            name_owner=t.owner,
            email_owner=t.email_owner,
            date_create=datetime.datetime.now()
        )
        values = {**token.dict()}
        query = set_token.insert().values(**values)
        await self.database.execute(query)


        responce = TokenOut(
            access_token=access_token,
            refresh_token=refresh_token
        )

        return responce
        
    async def refresh_token(self, token: TokenAuthIn) -> TokenAuthOut:
        """Создание нового jwt"""
        query = hub_token.select()
        refresh_token = await self.database.fetch_all(query=query)
        
        check_flag = False
        token_id = 0
        for item in refresh_token:
            parse_obj = HubTokenModel.parse_obj(item)
            if security.verify_hash_token(token.refresh_token, parse_obj.refresh_token):
                check_flag = True
                token_id = parse_obj.token_sk
        
        if check_flag:
            access_token=security.create_hash_token(token.refresh_token + token.password)
            responce = TokenAuthOut(
                access_token=security.create_hash_token(access_token)
            )
            values = {
                "access_token" : responce.access_token,
            }

            query = hub_token.update().where(hub_token.c.token_sk==token_id).values(**values)
            await self.database.execute(query=query)

            return responce
        else:
            return False
        

    async def verify_refresh_token(self, refresh_token) -> int:
        """Проверка подлиности refresh токена"""
        query = hub_token.select()
        responce_db = await self.database.fetch_all(query=query)
        
        for item in responce_db:
            parse_obj = HubTokenModel.parse_obj(item)
            if security.verify_hash_token(refresh_token, parse_obj.refresh_token):
                return parse_obj.token_sk
        return None
        
    async def verify_access_token(self, access_token) -> int:
        """Проверка подлиности access токена (без хеширования)"""
        query = hub_token.select().where(hub_token.c.access_token==access_token)
        responce_db = await self.database.fetch_one(query)
        
        
        # print("ACCESS_TOKEN", responce_db)
        if responce_db is not None:
            responce_db = HubTokenModel.parse_obj(responce_db)
            return responce_db.token_sk
        else:
            print("raise error")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")


    async def delete_token(self):
        """Удаление токена"""
    
    
    def calculating_duration_token(self):
        return datetime.datetime.now() + datetime.timedelta(days=365)
