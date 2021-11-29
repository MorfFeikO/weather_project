"""Rabbitmq host reconnect module.

Functions:
    connection_wait(host, loop, state=False)
"""
import logging

import lxml.etree
from lxml.etree import XMLSyntaxError, XMLSchemaValidateError
from aio_pika import connect, ExchangeType

from app import weather_schema, error_data


class DirectExchange:
    """Direct exchange class."""
    def __init__(self, loop, host=None, name="weather"):
        self.loop = loop
        self.host = host
        self.name = name
        self._type = ExchangeType.DIRECT
        self.connection = None
        self.channel = None

    async def _set_connection(self):
        """Set connection to rabbitmq server."""
        self.connection = await self.connection_wait()

    async def declare_exc(self):
        """Declare direct exchange.

        :return exchange
        """
        await self._set_connection()
        self.channel = await self.connection.channel()
        return await self.channel.declare_exchange(self.name, self._type)

    async def declare_queue(self, queue):
        """Declare queue.

        :return queue
        """
        return await self.channel.declare_queue(queue, durable=True)

    async def connection_wait(self, state=False):
        """Connect to rabbitmq host.

        :param state: default: False
        :return connection
        """
        connection = ""
        while not state:
            try:
                connection = await connect(host=self.host, loop=self.loop)
                state = True
            except ConnectionError:
                state = False
        return connection


def validate_xml(schema, xml):
    """Validate xml with it's schema."""
    xml_validator = lxml.etree.XMLSchema(file=schema)
    return xml_validator.validate(lxml.etree.fromstring(xml))


def validate(fun, schema=weather_schema):
    """Xml validator wrapper."""
    def wrapper(xml_data):
        try:
            if validate_xml(schema, xml_data):
                return fun(xml_data)
            logging.error("XML data not valid with schema.")
        except XMLSyntaxError as err:
            logging.error(str(err))
    return wrapper
