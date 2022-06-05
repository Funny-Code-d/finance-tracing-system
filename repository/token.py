from fastapi import HTTPException, status, Depends
from models.token import TokenIn, Token, TokenOut, TokenAuthIn, TokenHash, TokenDelete
from core.security import create_hash_token, verify_hash_token
from orm.token_map import TokenEntity
import datetime
from typing import List


class TokenRepository():

    def __init__(self, orm_obj):
        self.db_orm: TokenEntity = orm_obj
    

    async def create_token(self, token: TokenIn) -> TokenOut:
        
        access_token = create_hash_token(token.owner + token.email_owner)
        refresh_token = create_hash_token(token.owner + token.email_owner + token.password)

        t = Token(
            access_token=access_token,
            refresh_token=create_hash_token(refresh_token),
            owner=token.owner,
            email_owner=token.email_owner,
            date_create=datetime.datetime.now(),
        )

        token_sk = await self.db_orm.add(token=t)
        
        return TokenOut(
            token_sk=token_sk,
            access_token=access_token,
            refresh_token=refresh_token
        )


    async def refresh_token(self, token: TokenAuthIn) -> TokenHash:
        """Создание нового jwt"""
        
        token_sk = await self.verify_refresh_token(token.access_token, token.refresh_token)

        if token_sk is not None:
            new_access_token = create_hash_token(token.access_token)
            
            new_token = TokenHash(
                token_sk=token_sk,
                access_token=new_access_token
            )
            
            await self.db_orm.update_access_token(new_token)
            return new_token
        else:
            return False
            
            
        

    async def verify_refresh_token(self, access_token: str, refresh_token: str) -> int:
        """Проверка подлиности refresh токена"""
        token_sk = await self.db_orm.get_token_id(access_token)
        try:
            tokens = TokenHash.parse_obj(await self.db_orm.get_token(token_sk=token_sk))
            hash_refresh_token = tokens.refresh_token
        except ValueError:
            return None
        
        if verify_hash_token(refresh_token, hash_refresh_token):
            return token_sk
        else:
            return None
        
    async def verify_refresh_token_by_id(self, token_sk: str, refresh_token: str) -> int:
        """Проверка подлиности refresh токена"""
        try:
            tokens = TokenHash.parse_obj(await self.db_orm.get_token(token_sk=token_sk))
            hash_refresh_token = tokens.refresh_token
        except ValueError:
            return None
        
        if verify_hash_token(refresh_token, hash_refresh_token):
            return True
        else:
            return False

        
    async def verify_access_token(self, access_token) -> int:
        """Проверка подлиности access токена (без хеширования)"""
        token_sk = await self.db_orm.get_token_id(access_token)

        if token_sk is not None:
            return token_sk
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token did not pass the auth")


    async def delete_token(self, token: TokenDelete):
        """Удаление токена"""
        token_sk = await self.verify_refresh_token(token.access_token, token.refresh_token)
        if token_sk:
            await self.db_orm.delete(token_sk)
        return True
    
    
    def calculating_duration_token(self):
        return datetime.datetime.now() + datetime.timedelta(days=365)
