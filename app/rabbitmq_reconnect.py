"""Rabbitmq host reconnect module.

Functions:
    connection_wait(host, loop, state=False)
"""
from aio_pika import connect


async def connection_wait(host, loop, state=False):
    """Connect to rabbitmq host.
    :param host: str
    :param loop: eventloop
    :param state: default: False
    :return connection
    """
    connection = ""
    while not state:
        try:
            connection = await connect(host=host, loop=loop)
            state = True
        except ConnectionError:
            state = False
    return connection
