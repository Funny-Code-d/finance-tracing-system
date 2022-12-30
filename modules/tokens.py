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
