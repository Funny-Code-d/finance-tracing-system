import datetime
from fastapi import status, Response
from typing import Union

from .base import BaseRepository
from models.user import User, UserIn, UserPatch, UserRegistartion, HubCustomerModel, SetCustomerModel, LinkTokenCustomer, UserAuth, DeleteUser
from modules.tokens import access_control
from db.hubs import h_customer, h_token
from db.links import l_token_customer
from db.sattelites import s_customer


class UserRepository(BaseRepository):

    @access_control
    async def get_all(self, token: str):
        pass

    @access_control
    async def auth(self, user_data: UserAuth, token: str) -> bool:
        pass

    @access_control
    async def get_by_telegram(self, telegram_id: int, token: str):
        """Получение пользователя по Telegram id"""
        hub_user = self.session.query(h_customer).filter(h_customer.telegram_id == telegram_id).first()
        hub_token = self.session.query(h_token).filter(h_token.access_token == token).first()

        if not hub_user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        valid_user = self.session.query(l_token_customer).filter(
            l_token_customer.token_sk == hub_token.token_sk,
            l_token_customer.customer_sk == hub_user.customer_sk
        ).first()

        if valid_user:
            sat_user = self.session.query(s_customer).filter(
                s_customer.customer_sk == hub_user.customer_sk
            ).first()

            return {
                "id": hub_user.customer_sk,
                "first_name": sat_user.first_name,
                "last_name": sat_user.last_name,
                "email": hub_user.email,
                "telegram_id": hub_user.telegram_id
            }
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    @access_control
    async def get_by_id(self, user_id: int, token: str) -> Union[Response, dict]:
        """Получение пользователя по ID"""
        hub_user = self.session.query(h_customer).filter(h_customer.customer_sk == user_id).first()
        hub_token = self.session.query(h_token).filter(h_token.access_token == token).first()

        if not hub_user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        valid_user = self.session.query(l_token_customer).filter(
            l_token_customer.token_sk == hub_token.token_sk,
            l_token_customer.customer_sk == hub_user.customer_sk
        ).first()

        if valid_user:
            sat_user = self.session.query(s_customer).filter(
                s_customer.customer_sk == hub_user.customer_sk
            ).first()

            return {
                "id": hub_user.customer_sk,
                "first_name": sat_user.first_name,
                "last_name": sat_user.last_name,
                "email": hub_user.email,
                "telegram_id": hub_user.telegram_id
            }
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    @access_control
    async def get_by_email(self, email: str, token: str) -> Union[Response, dict]:
        """Получение пользователя по Email"""
        hub_user = self.session.query(h_customer).filter(h_customer.email == email).first()
        hub_token = self.session.query(h_token).filter(h_token.access_token == token).first()

        if not hub_user:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        valid_user = self.session.query(l_token_customer).filter(
            l_token_customer.token_sk == hub_token.token_sk,
            l_token_customer.customer_sk == hub_user.customer_sk
        ).first()

        if valid_user:
            sat_user = self.session.query(s_customer).filter(
                s_customer.customer_sk == hub_user.customer_sk
            ).first()

            return {
                "id": hub_user.customer_sk,
                "first_name": sat_user.first_name,
                "last_name": sat_user.last_name,
                "email": hub_user.email,
                "telegram_id": hub_user.telegram_id
            }
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    @access_control
    async def create_user(self, u: UserRegistartion, token: str) -> Union[Response, dict]:
        """Создание пользователя"""
        is_already = self.session.query(h_customer).filter(h_customer.email == u.email).first()

        # Такой пользователь уже существует
        if is_already:
            return Response(status_code=status.HTTP_409_CONFLICT)

        hub_token = self.session.query(h_token).filter(h_token.access_token == token).first()
        date_now = datetime.datetime.now()
        hub_user = h_customer(
            email=u.email,
            telegram_id=u.telegram_id,
            password=u.password,
            load_dttm=date_now
        )
        self.session.add(hub_user)
        self.session.commit()

        sat_user = s_customer(
            customer_sk=hub_user.customer_sk,
            first_name=u.first_name,
            last_name=u.last_name,
            load_dttm=date_now
        )
        self.session.add(sat_user)

        link_user = l_token_customer(
            token_sk=hub_token.token_sk,
            customer_sk=hub_user.customer_sk,
            load_dttm=date_now
        )
        self.session.add(link_user)
        self.session.commit()

        return {
            "id": hub_user.customer_sk
        }

    @access_control
    async def put_user(self, u: User, token: str) -> User:
        """Изменение информации о пользователе"""
        pass

    @access_control
    async def patch_user(self, u: UserPatch, token: str) -> User:
        """Изменение информации о пользователе"""
        pass

    @access_control
    async def delete_user(self, u: DeleteUser, token: str) -> User:
        pass
