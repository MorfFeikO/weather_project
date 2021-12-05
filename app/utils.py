"""Rabbitmq host reconnect module.

Functions:
    connection_wait(host, loop, state=False)
"""
import logging
import time
import lxml.etree

from lxml.etree import XMLSyntaxError, XMLSchemaValidateError
from aio_pika import connect, ExchangeType
from aio_pika import IncomingMessage

from app import weather_schema, schema_api


class DirectExchange:
    """Direct singleton exchange class."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls._instance = super(DirectExchange, cls).__new__(cls)
        return cls._instance

    def __init__(self, loop, host=None, name="weather"):
        self.loop = loop
        self.host = host
        self.name = name
        self._type = ExchangeType.DIRECT
        self.connection = None
        self.channel = None

    async def _set_connection(self):
        """Set connection to rabbitmq server."""
        self.connection = await self._connection_wait()

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

    async def _connection_wait(self):
        """Connect to rabbitmq host.

        :return connection
        """
        start = time.time()
        while True:
            try:
                connection = await connect(host=self.host, loop=self.loop)
                return connection
            except ConnectionError:
                if time.time() - start >= 5:
                    break
        raise ConnectionError("""
        Couldn't connect to RabbitMQ server. You view previously stored data.
        """)


def validate_xml(schema, xml):
    """Validate xml with it's schema."""
    xml_validator = lxml.etree.XMLSchema(file=schema)
    return xml_validator.validate(lxml.etree.fromstring(xml))


async def validate_after_rabbit(fun, schema=weather_schema):
    """Xml validator wrapper."""
    async def wrapper(message: IncomingMessage):
        try:
            if validate_xml(schema, message.body):
                return fun(message.body)
            raise XMLSchemaValidateError("XML data not valid with schema.")
        except (XMLSyntaxError, XMLSchemaValidateError) as exc:
            logging.error(f"ID: {message.message_id}."
                          f" ROUTE_KEY: {message.routing_key}."
                          f" {str(exc)}")
    return wrapper


def process_message(callback):
    """RabbitMQ callback wrapper."""
    async def wrapper(message: IncomingMessage):
        async with message.process():
            return await callback(message.body)
    return wrapper


def validate_api_xml(fun, schema=schema_api):
    """Xml validator wrapper."""
    def wrapper(data):
        try:
            if validate_xml(schema, data):
                return fun(data)
            raise XMLSchemaValidateError(
                "XMLSchemaValidationError."
                " Something went wrong. XML data is not valid."
            )
        except XMLSyntaxError as exc:
            logging.error(f"{str(exc)}")
    return wrapper
