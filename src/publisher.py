from evestidor_event_stream import EventStream

from src.domain import StockPrice


class Publisher:

    def publish_stock_price(self, stock_price: StockPrice):
        handler = EventStream(host='evestidor-event-stream')
        handler.send(
            exchange_name='stock_prices',
            routing_key='stock.prices.update',
            data={
                'symbol': stock_price.symbol,
                'date': stock_price.date.strftime('%Y-%m-%d'),
                'price': stock_price.price,
            }
        )
