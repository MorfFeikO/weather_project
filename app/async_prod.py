import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType
from app.models import W


async def produce(loop, message_body, queue_name):
    # Perform connection
    connection = await connect(host='rabbitmq', loop=loop)
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


if __name__ == '__main__':
    dat = [
        W('Ukraine', b'Lviv weather'),
        W('Ukraine', b'Lviv weather'),
        W('UK', b'UK weather'),
        W('USA', b'USA weather'),
        W('Ukraine', b'Ukraine weather'),
        W('Italy', b'Italy weather'),
        W('China', b'China weather'),
        W('Ukraine', b'Ukraine weather'),
        W('China', b'China weather'),
        W('Italy', b'Italy weather'),
        W('Italy', b'Italy weather'),
        W('Italy', b'Italy weather'),
        W('China', b'China weather'),
    ]
    for el in dat:
        main(el)
