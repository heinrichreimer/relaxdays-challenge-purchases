from dataclasses import dataclass
from datetime import datetime


@dataclass
class Purchase:
    supplier: str
    article_id: int
    amount: int
    time: datetime
