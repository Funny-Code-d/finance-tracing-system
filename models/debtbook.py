from pydantic import BaseModel
from typing import List, Optional
import datetime


class DebtbookHistoryItem(BaseModel):
    date: datetime.datetime
    amount: float
    description: Optional[str]


class DebtbookHistory(BaseModel):
    debtor_name: str
    take: List[DebtbookHistoryItem]
    give: List[DebtbookHistoryItem]


class DebtbookWrite(DebtbookHistoryItem):
    user_id: int
    debtor_name: int
    type_action: str
    date: datetime.datetime
    amount: float
    description: Optional[str]
