"""Async rabbitmq calls consumer."""
import sys
import asyncio
import logging
import typer

from app import rabbitmq_host
from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file
from app.utils import DirectExchange


async def main(loop):
    """Connect consumer to rabbitmq and start listening.

    :param loop:
        Running event loop.
    """
    # Declare exchange
    exchange = DirectExchange(loop=loop, host=rabbitmq_host)
    weather_exchange = await exchange.declare_exc()

    # Declaring queue
    queues = {}
    for queue in consumer_list:
        queues[queue] = await exchange.declare_queue(queue=queue)

    # Start consume
    for queue_name, queue in queues.items():
        await queue.bind(weather_exchange, routing_key=queue_name)
        await queue.consume(consumer_list[queue_name])


def consumer_run():
    """Start consumer to listen the queue."""
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
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
