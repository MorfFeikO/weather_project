import asyncio
import typer
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from aio_pika import connect, IncomingMessage, ExchangeType

from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file
# from db_requests import save_data_to_db
# from files_requests import save_data_to_file


async def on_message_db(message: IncomingMessage):
    async with message.process():
        save_data_to_db(message.body)


async def on_message_txt(message: IncomingMessage):
    async with message.process():
        save_data_to_file(message.body)


# async def on_message(message: IncomingMessage):
#    async with message.process():
#        country = message.routing_key
#        CONSUMER_LIST[country](message.body)


async def main(loop,
               queue_name,
               callback
               ):
    # Perform connection
    connection = await connect(host='rabbitmq', loop=loop)
    # connection = await connect(loop=loop)

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
    # typer.run(consumer_run)
    # print('Ukraine listening')
    # consumer_run('Ukraine')
    # print('UK listening')
    # consumer_run('UK')
    # print('Italy listening')
    # consumer_run('Italy')
    # print('USA listening')
    # consumer_run('USA')
    print('China listening')
    consumer_run('China')
