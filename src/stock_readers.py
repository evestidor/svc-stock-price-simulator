import json
from abc import ABC, abstractmethod
from typing import List

from src.domain import Stock


class StockReader(ABC):

    @abstractmethod
    def read_stocks(self) -> List[Stock]:
        pass


class JSONStockReader(StockReader):

    def __init__(self, path: str):
        self._path = path
        self._cached_json = None

    def read_stocks(self) -> Stock:
        if self._cached_json is None:
            self._cached_json = json.loads(open(self._path, 'r+').read())
        return self._cached_json
