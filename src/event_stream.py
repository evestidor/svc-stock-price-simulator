import json
from typing import Callable

import pika


class ConnectionHandler:

    def __init__(self, host=None):
        self._parameters = pika.ConnectionParameters(host=host)
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = pika.BlockingConnection(self._parameters)
        return self._connection

    def __enter__(self):
        return self.connection

    def __exit__(self, *args):
        self.connection.close()


class EventHandler:

    def __init__(self, host=None, connection_handler=ConnectionHandler):
        self._host = host
        self._connection_handler = connection_handler

    def publish(
        self,
        exchange_name: str,
        routing_key: str,
        data: dict,
    ):
        with self._connection_handler(self._host) as conn:
            channel = conn.channel()
            channel = self._declare_exchange(channel, exchange_name)
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=json.dumps(data),
                # Delivery mode 2 makes the broker save the message to disk.
                # This will ensure that the message be restored on reboot even
                # if RabbitMQ crashes before having forwarded the message.
                properties=pika.BasicProperties(delivery_mode=2)
            )

    def consume(
        self,
        exchange_name: str,
        routing_key: str,
        callback: Callable,
    ):
        with self._connection_handler(self._host) as conn:
            channel = conn.channel()
            channel = self._declare_exchange(channel, exchange_name)
            channel, queue_name = self._declare_queue(channel)
            channel.queue_bind(
                queue=queue_name,
                exchange=exchange_name,
                routing_key=routing_key,
            )
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=True,
            )
            channel.start_consuming()

    def _declare_exchange(self, channel, exchange_name):
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic',
            durable=True,
        )
        return channel

    def _declare_queue(self, channel):
        result = channel.queue_declare(
            queue='',
            durable=True,
            auto_delete=False,
        )
        return channel, result.method.queue
