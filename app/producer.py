"""Async rabbitmq calls producer.

Functions:
    produce(loop, message_body, queue_name)
        Connect producer to rabbitmq and deliver message.
"""
from aio_pika import Message, DeliveryMode

from app import rabbitmq_host
from app.utils import DirectExchange


async def producer(loop, message_body, queue_name):
    """Connect producer to rabbitmq and deliver message.

    :param loop:
        Running event loop.
    :param message_body: bytes
        Weather data (xml format in bytes string).
    :param queue_name: str
        Name of the queue (name of the country).
    """
    # Declare exchange
    exchange = DirectExchange(loop=loop, host=rabbitmq_host)
    weather_exchange = await exchange.declare_exc()

    message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)

    # Sending the message
    await weather_exchange.publish(message, routing_key=queue_name)

    # await connection.close()
    await exchange.connection.close()
