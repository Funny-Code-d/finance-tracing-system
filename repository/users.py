import datetime
from fastapi import status, Response
from typing import Union
from sqlalchemy import text

from .base import BaseRepository
from models.user import User, UserIn, UserPatch, UserRegistartion, HubCustomerModel, SetCustomerModel, LinkTokenCustomer, UserAuth, DeleteUser
from modules.tokens import access_control
from db.hubs import h_customer, h_token
from db.links import l_token_customer
from db.sattelites import s_customer
from db.base import Engine
from core.security import hash_passwd, verify_hash_passwd


class UserRepository(BaseRepository):

    async def check_link_token_user(self, token, user_id) -> bool:
        query = f"""
            select t1.email
                from h_customer t1 join l_token_customer t2 on t1.customer_sk = t2.customer_sk
                join h_token t3 on t2.token_sk = t3.token_sk
                where t3.access_token = '{token}' and t1.customer_sk = {user_id}
        """
        with Engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            if result is None:
                return False
            else:
                return True

    @access_control
    async def get_all(self, token: str):
        query = f"""
            select t1.*, t4.* from  
                h_customer t1 join l_token_customer t2 on t1.customer_sk = t2.customer_sk
                join h_token t3 on t2.token_sk = t3.token_sk
                join s_customer t4 on t1.customer_sk = t4.customer_sk
                where t3.access_token = '{token}';
        """
        with Engine.connect() as conn:
            data = conn.execute(text(query))
            result = list()
            for item in data:
                item_list = {
                    "user_id": item['customer_sk'],
                    "first_name": item['first_name'],
                    "last_name": item['last_name'],
                    "email": item['email'],
                    "password": item['password'],
                    "telegram_id": item['telegram_id'],
                    "load_dttm": item['load_dttm']
                }
                result.append(item_list)
            return {
                "users": result
            }

    @access_control
    async def auth(self, user_data: UserAuth, token: str) -> Response:
        query = f"""
            select t1.email, t1.password
                from h_customer t1 join l_token_customer t2 on t1.customer_sk = t2.customer_sk
                join h_token t3 on t2.token_sk = t3.token_sk
                where t3.access_token = '{token}' and t1.email = '{user_data.email}'
        """

        with Engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            if result is None:
                return Response(status_code=status.HTTP_404_NOT_FOUND)
            password = result['password']
            if verify_hash_passwd(user_data.passwd, password):
                return Response(status_code=status.HTTP_200_OK)
            else:
                return Response(status_code=status.HTTP_401_UNAUTHORIZED)

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
            password=hash_passwd(u.password),
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
    async def put_user(self, u: User, token: str) -> Response:
        """Изменение информации о пользователе"""
        if not await self.check_link_token_user(token, u.id):
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        sat = self.session.query(s_customer).filter(s_customer.customer_sk == u.id).first()
        hub = self.session.query(h_customer).filter(h_customer.customer_sk == u.id).first()

        sat.first_name = u.first_name
        sat.last_name = u.last_name
        hub.email = u.email
        hub.telegram_id = u.telegram_id

        self.session.commit()

        return Response(status_code=status.HTTP_200_OK)

    @access_control
    async def patch_user(self, u: UserPatch, token: str) -> Response:
        """Изменение информации о пользователе"""
        if not await self.check_link_token_user(token, u.customer_sk):
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        sat = self.session.query(s_customer).filter(s_customer.customer_sk == u.customer_sk).first()
        hub = self.session.query(h_customer).filter(h_customer.customer_sk == u.customer_sk).first()

        if u.email is not None:
            hub.email = u.email

        if u.first_name is not None:
            sat.first_name = u.first_name

        if u.last_name is not None:
            sat.last_name = u.last_name

        if u.telegram_id is not None:
            hub.telegram_id = u.telegram_id

        self.session.commit()

        return Response(status_code=status.HTTP_200_OK)



    @access_control
    async def delete_user(self, u: DeleteUser, token: str) -> Response:
        if not await self.check_link_token_user(token, u.customer_sk):
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        sat = self.session.query(s_customer).filter(s_customer.customer_sk == u.customer_sk).first()
        hub = self.session.query(h_customer).filter(h_customer.customer_sk == u.customer_sk).first()
        link = self.session.query(l_token_customer).filter(l_token_customer.customer_sk == u.customer_sk).first()

        self.session.delete(sat)
        self.session.delete(link)

        self.session.commit()

        self.session.delete(hub)

        self.session.commit()

        return Response(status_code=status.HTTP_200_OK)
