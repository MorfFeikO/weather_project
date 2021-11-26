"""Async rabbitmq calls producer.

Functions:
    produce(loop, message_body, queue_name)
        Connect producer to rabbitmq and deliver message.
"""
from aio_pika import Message, DeliveryMode, ExchangeType

from app.rabbitmq_reconnect import connection_wait


async def produce(loop, message_body, queue_name):
    """Connect producer to rabbitmq and deliver message.

    :param loop:
        Running event loop.
    :param message_body: bytes
        Weather data (xml format in bytes string).
    :param queue_name: str
        Name of the queue (name of the country).
    """
    # Perform connection
    connection = await connection_wait(host="rabbitmq", loop=loop)

    # Creating a channel
    channel = await connection.channel()
    weather_exchange = await channel.declare_exchange("weather", ExchangeType.DIRECT)
    message = Message(message_body, delivery_mode=DeliveryMode.PERSISTENT)

    # Sending the message
    await weather_exchange.publish(message, routing_key=queue_name)

    await connection.close()
