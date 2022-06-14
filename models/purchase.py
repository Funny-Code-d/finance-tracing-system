from pydantic import BaseModel
from typing import List, Optional
import datetime


class PurchaseItem(BaseModel):
    name_product: str
    price: float
    quantity: int
    description: Optional[str]


class Purchase(BaseModel):
    group_id: str
    name_store: str
    total_amount: float
    category_id: str
    date: datetime.datetime
    items: List[PurchaseItem]


class PurchaseOut(BaseModel):
    """Модель для вывода или получения ручным вводом покупок"""
    purchase_id: int
    data: Purchase


class PurchaseData(BaseModel):
    """Модель для получения информации по чеку из ФНС"""
    fn: str
    fd: str
    fpd: str
    type: int
    date: datetime.datetime
    amount: int


class PurchaseIn(PurchaseData):
    """Модель для добавления новой покупки"""
    token_sk: Optional[int]
    customer_sk: int
    group_id: str
    
    
class DeletePurchase(BaseModel):
    """Модель для удаления покупки"""
    token_sk: Optional[int]
    customer_sk: int
    group_id: str
    purchase_id: int
