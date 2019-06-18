import random
from abc import ABC, abstractmethod
from typing import List

from src.domain import Stock
from src.stock_readers import StockReader


class StockChooser(ABC):

    @abstractmethod
    def choose(self) -> Stock:
        pass


class RandomStockChooser:

    def __init__(self, reader: StockReader):
        self._reader = reader
        self._seen_stocks = set()

    def choose(self) -> Stock:
        stocks = self._get_stocks()
        choosen_stock = self._pick_stock(stocks)
        self._update_seen_stocks(choosen_stock, stocks)
        return choosen_stock

    def _get_stocks(self):
        return [
            x for x in self._read_and_parse_stocks()
            if x.symbol not in self._seen_stocks
        ]

    def _read_and_parse_stocks(self) -> List[Stock]:
        return [self._parse_stock(x) for x in self._reader.read_stocks()]

    def _parse_stock(self, stock: dict) -> Stock:
        return Stock(
            symbol=stock['symbol'],
            min_price=stock['min_price'],
            max_price=stock['max_price'],
        )

    def _pick_stock(self, stocks: List[Stock]) -> Stock:
        index = random.randint(0, len(stocks) - 1)
        return stocks[index]

    def _update_seen_stocks(self, choosen: Stock, stocks: List[Stock]):
        if len(stocks) < 8:
            self._mark_oldest_stocks_as_unseen()
        self._mark_as_seen(choosen)

    def _mark_as_seen(self, stock: Stock):
        self._seen_stocks.add(stock.symbol)

    def _mark_oldest_stocks_as_unseen(self):
        stocks = list(self._seen_stocks)
        del stocks[0:4]
        self._seen_stocks = set(stocks)
