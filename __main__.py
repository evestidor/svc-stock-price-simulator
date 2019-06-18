import time
import logging

from src.stock_price_generator import StockPriceGenerator
from src.stock_choosers import RandomStockChooser
from src.stock_readers import JSONStockReader
from src.publisher import Publisher


logging.basicConfig(level=logging.INFO)

pika_logger = logging.getLogger('pika')
pika_logger.setLevel(logging.CRITICAL)

app_logger = logging.getLogger('stock-prices-tracker')


class LoggedPublisher(Publisher):

    def publish_stock_price(self, stock_price):
        app_logger.info(
            f'Publishing [{stock_price.symbol}] at ({stock_price.price})'
        )
        super().publish_stock_price(stock_price)


def main():
    reader = JSONStockReader(path='resources/stocks.json')
    chooser = RandomStockChooser(reader)
    price_generator = StockPriceGenerator(chooser)

    while True:
        stock_price = price_generator.generate()
        LoggedPublisher().publish_stock_price(stock_price)
        time.sleep(0.5)


main()
