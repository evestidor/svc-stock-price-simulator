import datetime
from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    min_price: float
    max_price: float


@dataclass
class StockPrice:
    symbol: str
    price: float
    date: datetime.date
