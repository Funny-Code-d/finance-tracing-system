from sqlalchemy import text
from fastapi import Response, status
from sqlalchemy.orm.session import sessionmaker

from db.hubs import h_token
from db.base import Engine


def access_control(func):
    async def wrapper(self, *args, **kwargs):
        session = sessionmaker(bind=Engine)()
        token = session.query(h_token).filter(h_token.access_token == kwargs['token'])
        if token:
            return await func(self, *args, **kwargs)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    return wrapper


def access_group(func):
    async def wrapper(self, *args, **kwargs):
        query = "SELECT token_sk FROM h_token"
        with Engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            token_sk = result[0]

            query = f"""
                SELECT 1 FROM l_token_customer t1
                    JOIN l_pull_group t2 on t1.customer_sk=t2.customer_sk
                    WHERE t1.token_sk = {token_sk} AND t2.group_sk = '{kwargs['group_sk']}' 
                    AND t1.customer_sk = {kwargs['customer_sk']}
            """
            result = conn.execute(text(query)).fetchone()
            if result:
                return await func(self, *args, **kwargs)
            else:
                return Response(status_code=status.HTTP_403_FORBIDDEN)
            
    return wrapper
