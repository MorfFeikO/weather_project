"""Async rabbitmq calls consumer."""
import sys
import asyncio
import logging
import pathlib
import typer

# from aio_pika import IncomingMessage

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from app import rabbitmq_host
from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file
from app.utils import DirectExchange


# async def on_message_db(message: IncomingMessage):
#     """Save to database callback.
#
#     :param message: IncomingMessage
#         Single message from rabbitmq with database data in body.
#     """
#     async with message.process():
#         save_data_to_db(message.body)
#
#
# async def on_message_txt(message: IncomingMessage):
#     """Save to file callback.
#
#     :param message: IncomingMessage
#         Single message from rabbitmq with file data in body.
#     """
#     async with message.process():
#         save_data_to_file(message.body)


# async def main(loop, queue_name, callback):
#     """Connect consumer to rabbitmq and start listening.
#
#     :param loop:
#         Running event loop.
#     :param queue_name: str
#         Name of the queue (name of the country).
#     :param callback: func
#         Callback function depends on queue name.
#     """
#     # Declare exchange
#     exchange = DirectExchange(loop=loop, host=rabbitmq_host)
#     weather_exchange = await exchange.declare_exc()
#
#     # Declaring queue
#     queue = await exchange.declare_queue(queue=queue_name)
#     await queue.bind(weather_exchange, routing_key=queue_name)
#
#     # Start listening the random queue
#     await queue.consume(callback)


# def consumer_run(queue_name):
#     """Start consumer to listen the queue.
#
#     :param queue_name: str
#         Name of the queue (name of the country).
#     """
#     loop = asyncio.get_event_loop()
#     if queue_name not in consumer_list:
#         queue_name = "other"
#
#     try:
#         loop.create_task(main(
#             loop,
#             queue_name=queue_name,
#             callback=consumer_list[queue_name]
#         ))
#         loop.run_forever()
#     except ConnectionError as exc:
#         err_msg = {
#             "error": str(exc) + f". Queue {queue_name} didn't connect."
#         }
#         logging.error(err_msg)
#         sys.exit(1)


# consumer_list = {
#     "Ukraine": on_message_db,
#     "UK": on_message_db,
#     "Italy": on_message_txt,
#     "China": on_message_txt,
#     "USA": on_message_txt,
#     "other": on_message_db,
# }


async def main(loop):
    """Connect consumer to rabbitmq and start listening.

    :param loop:
        Running event loop.
    """
    # Declare exchange
    exchange = DirectExchange(loop=loop, host=rabbitmq_host)
    weather_exchange = await exchange.declare_exc()

    # Declaring queue
    for queue in consumer_list:
        queue = await exchange.declare_queue(queue=queue)
        await queue.bind(weather_exchange, routing_key=queue)
        await queue.consume(consumer_list[queue])


def consumer_run():
    """Start consumer to listen the queue."""
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main(loop))
        loop.run_forever()
    except ConnectionError as exc:
        err_msg = {
            "error": f"{str(exc)}. Worker didn't connect."
        }
        logging.error(err_msg)
        sys.exit(1)


consumer_list = {
    "Ukraine": save_data_to_db,
    "UK": save_data_to_db,
    "Italy": save_data_to_file,
    "China": save_data_to_file,
    "USA": save_data_to_file,
    "other": save_data_to_file,
}


if __name__ == "__main__":
    typer.run(consumer_run)
