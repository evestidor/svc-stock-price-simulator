import datetime
import random

from src.domain import Stock, StockPrice
from src.stock_choosers import StockChooser


class StockPriceGenerator:

    def __init__(self, chooser: StockChooser):
        self._chooser = chooser

    def generate(self) -> StockPrice:
        stock = self._chooser.choose()
        price = self._estimate_price(stock)
        return StockPrice(
            symbol=stock.symbol,
            price=price,
            date=datetime.date.today(),
        )

    def _estimate_price(self, stock: Stock) -> float:
        return round(random.uniform(stock.min_price, stock.max_price), 2)
