"""Rabbitmq host reconnect module.

Functions:
    connection_wait(host, loop, state=False)
"""
import logging

import lxml.etree
from lxml.etree import XMLSyntaxError, XMLSchemaValidateError
from aio_pika import connect

from app import weather_schema, error_data


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


def validate_xml(schema, xml):
    xml_validator = lxml.etree.XMLSchema(file=schema)
    return xml_validator.validate(lxml.etree.fromstring(xml))


def validate(f, schema=weather_schema):
    def wrapper(xml_data):
        try:
            if validate_xml(schema, xml_data):
                return f(xml_data)
            else:
                logging.error("XML data not valid with schema.")
                return f(error_data)
        except XMLSyntaxError as err:
            logging.error(str(err))
            return f(error_data)
    return wrapper
