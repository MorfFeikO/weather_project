import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType


async def connection_wait(host, loop, state=False):
    while not state:
        try:
            connection = await connect(host=host, loop=loop)
            state = True
        except ConnectionError:
            state = False
    return connection


async def produce(loop, message_body, queue_name):
    # Perform connection
    # connection = await connect(host='rabbitmq', loop=loop)
    connection = await connection_wait(host='rabbitmq', loop=loop)
    # connection = await connect(loop=loop)

    # Creating a channel
    channel = await connection.channel()
    weather_exchange = await channel.declare_exchange(
        "weather", ExchangeType.DIRECT
    )
    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    # Sending the message
    await weather_exchange.publish(
        message, routing_key=queue_name
    )

    await connection.close()


async def main(data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        produce(loop, message_body=data.xml_data, queue_name=data.country)
    )
