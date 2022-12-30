from fastapi import HTTPException, status, Depends, Response
from typing import Union

from models.token import TokenIn, Token, TokenOut, TokenAuthIn, TokenHash, TokenDelete
from core.security import create_hash_token, verify_hash_token, hash_passwd
import datetime
from .base import BaseRepository
from db.hubs import h_token
from db.links import l_token_customer
from db.sattelites import s_token
# from modules.tokens import tokens_decorator


class TokenRepository(BaseRepository):

    async def create_token(self, token_model: TokenIn) -> Union[TokenOut, bool]:

        break_flag = True

        while break_flag:

            access_token = create_hash_token(token_model.owner + token_model.email_owner)
            refresh_token = create_hash_token(token_model.owner + token_model.email_owner + token_model.password)

            is_already = self.session.query(h_token).filter(h_token.access_token == access_token).first()

            if not is_already:
                break_flag = False

                date_now = datetime.datetime.now()
                hub = h_token(
                    access_token=access_token,
                    refresh_token=hash_passwd(refresh_token),
                    load_dttm=date_now
                )
                self.session.add(hub)
                self.session.commit()

                sat = s_token(
                    token_sk=hub.token_sk,
                    name_owner=token_model.owner,
                    email_owner=token_model.email_owner,
                    load_dttm=date_now
                )
                self.session.add(sat)
                self.session.commit()

                if hub.token_sk:
                    return TokenOut(
                        token_sk=hub.token_sk,
                        access_token=access_token,
                        refresh_token=refresh_token
                    )
                else:
                    return False
            else:
                continue

    async def refresh_token(self, token_model: TokenAuthIn) -> Union[dict, Response]:
        """Создание нового jwt"""
        token_element = self.session.query(h_token).filter(h_token.access_token == token_model.access_token).first()
        if token_element:
            verify = verify_hash_token(token_model.refresh_token, token_element.refresh_token)
            if verify:
                new_token = create_hash_token(token_model.access_token)
                token_element.access_token = new_token
                self.session.commit()
                return {"new_access_token":  new_token}
            else:
                return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def delete_token(self, token_model: TokenDelete):
        """Удаление токена"""
        token_element = self.session.query(h_token).filter(
            h_token.access_token == token_model.access_token
        ).first()

        if token_element:
            print(token_element)
            link_token = self.session.query(l_token_customer).filter(
                l_token_customer.token_sk == token_element.token_sk
            ).all()
            print(link_token)
            if len(link_token) > 0:
                for item in link_token:
                    self.session.delete(item)
            self.session.delete(h_token)
            self.session.commit()
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
