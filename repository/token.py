from typing import List
from .base import BaseRepository
from models.token import TokenIn, Token, TokenOut, TokenAuthOut, TokenAuthIn
from db.token import token_table
from core import security
import datetime

class TokenRepository(BaseRepository):
    

    async def create_token(self, t: TokenIn) -> TokenOut:
        """Создание токена для нового пользователя"""

        access_token = security.create_hash_token(t.owner + t.email_owner)
        refresh_token = security.create_hash_token(t.owner + t.email_owner + t.password)
        token = Token(
            access_token=security.create_hash_token(access_token),
            refresh_token=security.create_hash_token(refresh_token),
            owner=t.owner,
            email_owner=t.email_owner,
            date_create=datetime.datetime.now(),
            date_refresh=datetime.datetime.now(),
            date_end=self.calculating_duration_token()
        )
        values = {**token.dict()}
        values.pop("token_id", None)

        query = token_table.insert().values(**values)
        token.token_id = await self.database.execute(query)

        responce = TokenOut(
            access_token=access_token,
            refresh_token=refresh_token
        )

        return responce
        
    async def refresh_token(self, token: TokenAuthIn) -> TokenAuthOut:
        """Создание нового jwt"""
        query = token_table.select()
        refresh_token = await self.database.fetch_all(query=query)
        
        check_flag = False
        token_id = 0
        for item in refresh_token:
            parse_obj = Token.parse_obj(item)
            if security.verify_hash_token(token.refresh_token, parse_obj.refresh_token):
                check_flag = True
                token_id = parse_obj.token_id
        
        if check_flag:
            access_token=security.create_hash_token(token.refresh_token + token.password)
            responce = TokenAuthOut(
                access_token=security.create_hash_token(access_token)
            )
            values = {
                "access_token" : responce.access_token,
                "date_refresh" : datetime.datetime.now()
            }

            query = token_table.update().where(token_table.c.token_id==token_id).values(**values)
            await self.database.execute(query=query)

            return responce
        else:
            return False
        

    async def verify_token(self, access_token):
        """Проверка подлиности токена"""
        query = token_table.select()
        responce_db = await self.database.fetch_all(query=query)
        
        for item in responce_db:
            parse_obj = Token.parse_obj(item)
            print(parse_obj.access_token, access_token, end='\n')
            if security.verify_hash_token(access_token, parse_obj.access_token):
                print(parse_obj.token_id)
                return parse_obj.token_id
        return False
        

    
    async def delete_token(self):
        """Удаление токена"""
    
    
    def calculating_duration_token(self):
        return datetime.datetime.now() + datetime.timedelta(days=365)