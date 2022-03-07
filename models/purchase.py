from pydantic import BaseModel
from typing import List, Optional
import datetime


class PurchaseItem(BaseModel):
    name_product: str
    amount: float
    quantity: int
    description: Optional[str]


class OnesPurchase(BaseModel):
    items: List[PurchaseItem]
    date: datetime.datetime
    total_amount: float
    category: str


class Purchase(BaseModel):
    """Модель для вывода или получения ручным вводом покупок"""
    user_id: int
    purchase_id: int
    purchase: List[OnesPurchase]
    range_days: Optional[int]


class ReceiptData(BaseModel):
    """Модель для получения информации по чеку из ФНС"""
    fn: str
    fd: str
    fpd: str
    type: int
    date: datetime.datetime
    amount: int


class AdditingPurchase(BaseModel):
    """Модель для добавления новой покупки"""
    user_id: int
    receipt: ReceiptData
    
    
class DeletePurchase(BaseModel):
    """Модель для удаления покупки"""
    user_id: int
    purchase_id: int    
