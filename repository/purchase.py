from .base import BaseRepository
from orm.purchase_map import PurchaseEntity
from models.purchase import ParsePay, PurchaseIn, PurchaseData, Purchase, PurchaseItem, DeletePurchase
from requests import post
from os import getenv
class PurchaseRepository(BaseRepository):
    

    def __init__(self, orm_obj):
        self.db_orm: PurchaseEntity = orm_obj


    async def request_fns(self, getting_data: PurchaseData) -> Purchase:
        token = getenv("TOKEN_FNS")
        data = {
            'fn': getting_data.fn,
            'fd' : getting_data.fd,
            'fp': getting_data.fp,
            't' : getting_data.t,
            'n' : getting_data.n,
            's' : getting_data.amount,
            'qr' : '0',
            'token': token
        }
        url = "https://proverkacheka.com/api/v1/check/get"
        req = post(url=url, data=data)
        if req.status_code == 200:
            # print(req.json())
            return ParsePay.parse_obj((req.json()['data']['json']))
        else:
            return False
    
    async def add_purchase(self, purchase_data: PurchaseIn) -> bool:
        """Добавление покупки"""
        if not await self.db_orm.check(purchase_data.token_sk, purchase_data.customer_sk, purchase_data.group_id):
            return False
        data = PurchaseData(
            fn=purchase_data.fn,
            fd=purchase_data.fd,
            fp=purchase_data.fp,
            t=purchase_data.t,
            n=purchase_data.n,
            amount=purchase_data.amount
        )

        receipt_info = await self.request_fns(data)
        print(receipt_info)
        result_items = list()

        for item in receipt_info.items:
            result_items.append(PurchaseItem(
                name_product=item.name,
                price=item.price,
                quantity=item.quantity,
            ))

        receipt = Purchase(
            group_id=purchase_data.group_id,
            name_store=receipt_info.user,
            total_amount=receipt_info.totalSum,
            category_id=purchase_data.category_id,
            items=result_items
        )

        responce_db = await self.db_orm.additing_purchase(receipt)
        return responce_db


        
    async def delete_purchase(self, purchase_data: DeletePurchase):
        if not await self.db_orm.check(purchase_data.token_sk, purchase_data.customer_sk, purchase_data.group_id):
            return False
        
        return await self.db_orm.delete_purchase(purchase_sk=purchase_data.purchase_id)
    
    async def get_purchase_today(self):
        """Получение покупок за сегодня"""
        
    async def get_purchase_week(self):
        """Получение покупок за неделю"""
    
    async def get_purchase_month(self):
        """Получение покупок за месяц"""
        
    async def get_purchase_year(self):
        """Получение покупок за год"""
    
    async def get_purchase_date_range(self):
        """Получение покупок за выбранный период"""
    
