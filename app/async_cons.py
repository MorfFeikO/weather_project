"""Async rabbitmq calls consumer."""
import sys
import asyncio
import typer

from aio_pika import IncomingMessage, ExchangeType

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file
from app.rabbitmq_reconnect import connection_wait


async def on_message_db(message: IncomingMessage):
    """Save to database callback.
    ...
    :param message: IncomingMessage
        Single message from rabbitmq with database data in body.
    """
    async with message.process():
        save_data_to_db(message.body)


async def on_message_txt(message: IncomingMessage):
    """Save to file callback.
    ...
    :param message: IncomingMessage
        Single message from rabbitmq with file data in body.
    """
    async with message.process():
        save_data_to_file(message.body)


async def main(loop, queue_name, callback):
    """Connect consumer to rabbitmq and start listening.
    ...
    :param loop:
        Running event loop.
    :param queue_name: str
        Name of the queue (name of the country).
    :param callback: func
        Callback function depends on queue name.
    """
    # Perform connection
    connection = await connection_wait(host='rabbitmq', loop=loop)

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare exchange
    direct_weather_exchange = await channel.declare_exchange(
        "weather", ExchangeType.DIRECT
    )

    # Declaring queue
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(direct_weather_exchange, routing_key=queue_name)

    # Start listening the random queue
    await queue.consume(callback)


def consumer_run(queue_name):
    """Start consumer to listen the queue.
    ...
    :param queue_name: str
        Name of the queue (name of the country).
    """
    loop = asyncio.get_event_loop()

    # there are workers for 5 countries in the list.
    # What about others if they will be added?
    # Additional worker for other countries is!
    if queue_name not in CONSUMER_LIST:
        queue_name = 'other'

    loop.create_task(main(
            loop,
            queue_name=queue_name,
            callback=CONSUMER_LIST[queue_name]
        ))
    loop.run_forever()


CONSUMER_LIST = {
    "Ukraine": on_message_db,
    "UK": on_message_db,
    "Italy": on_message_txt,
    "China": on_message_txt,
    "USA": on_message_txt,
    "other": on_message_db
}


if __name__ == '__main__':
    typer.run(consumer_run)
