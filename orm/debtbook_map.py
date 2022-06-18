from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_debtor, hun_debtbook
from db.settelites import set_debtbook_history
from db.links import link_debtor_debtbook, link_customer_debtor
from models.purchase import PurchaseIn, Purchase
from models.debtbook import DebtbookIn, DebtbookRecord, GetDebtbookRecord, PostTransaction, DebtorIn
from models.debtbook import DebtbookRecordHistoryItem, DebtbookRecordHistory
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime


class DebtbookEntity(BaseEntity):


    async def check_customer_debtor(self, customer_sk, debtor_sk):
        query = link_customer_debtor.select().where(
            link_customer_debtor.c.customer_sk==customer_sk,
            link_customer_debtor.c.debtor_sk==debtor_sk
        )
        if await self.database.fetch_one(query=query):
            return True
        else:
            return False

    async def add_debtor(self, debtor: DebtbookIn):
        values = {
            "debtor_name" : debtor.debtor_name
        }
        query = hub_debtor.insert().values(**values)
        debtor_sk = await self.database.execute(query=query)

        values = {
            "customer_sk" : debtor.customer_sk,
            "debtor_sk" : debtor_sk
        }

        query = link_customer_debtor.insert().values(**values)
        await self.database.execute(query=query)


        values = {
            "type_action" : "take",
            "total_amount" : 0
        }

        query = hun_debtbook.insert().values(**values)
        debtbook_take_sk = await self.database.execute(query=query)

        values = {
            "type_action" : "give",
            "total_amount" : 0
        }

        query = hun_debtbook.insert().values(**values)
        debtbook_give_sk = await self.database.execute(query=query)


        values = [
            {
                "debtor_sk" : debtor_sk,
                "debtbook_sk" : debtbook_take_sk
            },
            {
                "debtor_sk" : debtor_sk,
                "debtbook_sk" : debtbook_give_sk
            }
        ]

        for record in values:
            query = link_debtor_debtbook.insert().values(**record)
            await self.database.execute(query=query)
        

        return True
    

    async def get_all(self, customer_sk):
        query = select(
            hub_debtor.c.debtor_sk,
            hub_debtor.c.debtor_name,
            hun_debtbook.c.type_action,
            hun_debtbook.c.total_amount
        )
        query = query.join_from(link_customer_debtor, hub_debtor)
        query = query.join_from(hub_debtor, link_debtor_debtbook)
        query = query.join_from(link_debtor_debtbook, hun_debtbook)
        query = query.where(link_customer_debtor.c.customer_sk==customer_sk)

        responce_db = await self.database.fetch_all(query=query)
        result = list()
        for row in responce_db:
            result.append(DebtbookRecord.parse_obj(row))
        
        return GetDebtbookRecord(
            customer_sk=customer_sk,
            items=result
        )
                
                

    async def regist_transaction(self, debt_data: PostTransaction):

        query  = link_debtor_debtbook.select().where(
            link_debtor_debtbook.c.debtor_sk==debt_data.debtor_sk
        )
        responce_db = await self.database.fetch_all(query=query)

        debtbook_sk = dict()
        for row in responce_db:
            query = hun_debtbook.select().where(
                hun_debtbook.c.debtbook_sk==row['debtbook_sk']
            )
            res = await self.database.fetch_one(query=query)
            debtbook_sk[res['type_action']] = res['debtbook_sk']
        
        # print(debtbook_sk)

        query = hun_debtbook.select().where(
            hun_debtbook.c.debtbook_sk==debtbook_sk[debt_data.type_action]
        )
        responce_db = await self.database.fetch_one(query=query)
        
        values = dict()
        # print(debt_data)
        if debt_data.transaction == "add":
            values = {
                "total_amount" : float(responce_db['total_amount']) + float(debt_data.amount)
            }
        elif debt_data.transaction == "remove":
            values = {
                "total_amount" : float(responce_db['total_amount']) - float(debt_data.amount)
            }
        else:
            return False
        
        
        query = hun_debtbook.update().where(
            hun_debtbook.c.debtbook_sk==debtbook_sk[debt_data.type_action],
            hun_debtbook.c.type_action==debt_data.type_action
        ).values(**values)
        await self.database.fetch_one(query=query)

        values = {
            "debtbook_sk" : debtbook_sk[debt_data.type_action],
            "action" : debt_data.transaction,
            "amount" : debt_data.amount,
            "date_regist" : datetime.now()
        }
        query = set_debtbook_history.insert().values(**values)
        await self.database.execute(query=query)

    async def delete_debtor(self, debt_data: DebtorIn):
        query = hub_debtor.delete().where(
            hub_debtor.c.debtor_sk==debt_data.debtor_sk
        )

        await self.database.execute(query=query)
        return True

    async def get_history(self, debtor_sk):
        result_take = list()
        result_give = list()        
        for action in ("take", "give"):
            query = select(
                set_debtbook_history.c.action,
                set_debtbook_history.c.amount,
                set_debtbook_history.c.date_regist
            ).join_from(
                link_debtor_debtbook,
                hun_debtbook
            ).join_from(hun_debtbook, set_debtbook_history).where(
                link_debtor_debtbook.c.debtor_sk==debtor_sk,
                hun_debtbook.c.type_action==action
                ).order_by(set_debtbook_history.c.date_regist)

            responce_db = await self.database.fetch_all(query=query)

            for row in responce_db:
                if action == "take":
                    result_take.append(DebtbookRecordHistoryItem.parse_obj(row))
                else:
                    result_give.append(DebtbookRecordHistoryItem.parse_obj(row))

        
        
        query = hub_debtor.select().where(hub_debtor.c.debtor_sk==debtor_sk)
        responce_db = await self.database.fetch_one(query=query)
        
        return DebtbookRecordHistory(
            debtbook_sk=debtor_sk,
            debtor_name=responce_db['debtor_name'],
            take=result_take,
            give=result_give
        )