from databases import Database
from db.base import database
from db.links import link_token_customer, link_admin_group, link_pull_group

class BaseEntity():
    
    def __init__(self):
        self.database = database

    async def check(self, token_sk, customer_sk, group_sk):
        valid_customer = await self.check_token_customer(token_sk, customer_sk)
        if valid_customer:
            valid_group = await self.check_group_customer(customer_sk, group_sk)
            if valid_group:
                return True
            else:
                return False
        else:
            return False
    
    async def check_token_customer(self, token_sk: int, customer_sk: int) -> bool:
        query = link_token_customer.select().where(
            link_token_customer.c.customer_sk==customer_sk,
            link_token_customer.c.token_sk==token_sk
        )
        if await self.database.fetch_one(query=query):
            return True
        else:
            return False
        
    async def check_group_customer(self, customer_sk: int, group_sk: int) -> bool:
        query = link_admin_group.select().where(
            link_admin_group.c.customer_sk==customer_sk,
            link_admin_group.c.group_sk==group_sk
        )

        responce_db = await self.database.fetch_one(query=query)
        # Если пользователь админ группы, разрешить доступ
        if responce_db:
            return True
        else:
            query = link_pull_group.select(
                link_pull_group.c.customer_sk==customer_sk,
                link_pull_group.c.group_sk==group_sk
            )

            responce_db = await self.database.fetch_one(query=query)
            # Если пользователь состоит в группе, разрешить доступ
            if responce_db:
                return True
            else:
                return False