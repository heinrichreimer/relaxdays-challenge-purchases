from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Purchase:
    supplier: str
    article_id: int
    amount: int
    price: Decimal
    time: datetime
