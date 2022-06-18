from .base import BaseRepository
from orm.debtbook_map import DebtbookEntity
from models.purchase import ParsePay, PurchaseIn, PurchaseData, Purchase, PurchaseItem
from models.debtbook import DebtbookIn, PostTransaction, DebtorIn
from requests import post
from os import getenv


class DebtorRepository(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: DebtbookEntity = orm_obj

        
    async def add_debtor(self, debtor_data: DebtbookIn):
        if await self.db_orm.check_token_customer(debtor_data.token_sk, debtor_data.customer_sk):
            return await self.db_orm.add_debtor(debtor_data)
        else:
            return False
        
        

    async def get_all(self, token_sk: int, customer_sk: int):
        if await self.db_orm.check_token_customer(token_sk, customer_sk):
            return await self.db_orm.get_all(customer_sk)
        else:
            return False
        
    async def regist_transaction(self, debt_data: PostTransaction):
        """Получение покупок за неделю"""
        is_valid_debtor = await self.db_orm.check_customer_debtor(debt_data.customer_sk, debt_data.debtor_sk)
        is_valid_customer = await self.db_orm.check_token_customer(debt_data.token_sk, debt_data.customer_sk)
        
        if is_valid_customer and is_valid_debtor:
            return await self.db_orm.regist_transaction(debt_data=debt_data)
        else:
            return False
    
    async def delete_debtor(self, debt_data: DebtorIn):
        is_valid_debtor = await self.db_orm.check_customer_debtor(debt_data.customer_sk, debt_data.debtor_sk)
        is_valid_customer = await self.db_orm.check_token_customer(debt_data.token_sk, debt_data.customer_sk)
        
        if is_valid_customer and is_valid_debtor:
            return await self.db_orm.delete_debtor(debt_data=debt_data)
        else:
            return False
        
        
    async def get_history(self, token_sk, customer_sk, debtor_sk):
        is_valid_debtor = await self.db_orm.check_customer_debtor(customer_sk, debtor_sk)
        is_valid_customer = await self.db_orm.check_token_customer(token_sk, customer_sk)
        if is_valid_customer and is_valid_debtor:
            return await self.db_orm.get_history(debtor_sk)
        else:
            return False
    async def get_purchase_date_range(self):
        """Получение покупок за выбранный период"""
    