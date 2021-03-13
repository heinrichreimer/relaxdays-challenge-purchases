from dataclasses import dataclass


@dataclass
class Purchase:
    supplier: str
    article_id: int
    amount: int
