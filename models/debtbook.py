from pydantic import BaseModel
from typing import List, Optional
import datetime


class Debtbook(BaseModel):
    debtbor_sk: Optional[int]
    debtor_name: str
    telegram_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]

class DebtbookIn(Debtbook):
    token_sk: Optional[int]
    customer_sk: int
    

class DebtbookRecord(BaseModel):
    debtor_sk: Optional[int]
    debtor_name: Optional[str]
    type_action: str
    total_amount: Optional[float]

class GetDebtbookRecord(BaseModel):
    customer_sk: int
    items: List[DebtbookRecord]


class PostTransaction(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    debtor_sk: int
    type_action: str
    transaction: str
    amount: float




class DebtbookRecordHistoryItem(BaseModel):
    debtbook_sk: Optional[int]
    action: str
    amount: float
    date: datetime.datetime


class DebtbookRecordHistory(BaseModel):
    debtbook_sk: int
    debtor_name: str
    items: List[DebtbookRecordHistoryItem]