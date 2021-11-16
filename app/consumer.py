import os

import pika
import asyncio

from app import DEFAULT_INFO

from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file


def db_callback(ch, method, properties, body):
    save_data_to_db(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def txt_callback(ch, method, properties, body):
    save_data_to_file(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer_list = [
    {"callback": db_callback, "country": 'Ukraine'},
    {"callback": db_callback, "country": 'UK'},
    {"callback": txt_callback, "country": 'China'},
    {"callback": txt_callback, "country": 'Italy'},
    {"callback": txt_callback, "country": 'USA'},
]

db_callback_list = ['Ukraine', 'UK']
txt_callback_list = [country for country in DEFAULT_INFO if country not in db_callback_list]


connection2 = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'))
)
channel2 = connection2.channel()

for country in DEFAULT_INFO:
    channel2.queue_declare(queue=country, durable=True)


channel2.basic_qos(prefetch_count=1)  # can improve in 2 part of tutorial to messages not to stack


channel2.basic_consume(
    queue='Ukraine',
    on_message_callback=db_callback
)
channel2.basic_consume(
    queue='UK',
    on_message_callback=db_callback
)
channel2.basic_consume(
    queue='Italy',
    on_message_callback=txt_callback
)
channel2.basic_consume(
    queue='China',
    on_message_callback=txt_callback
)
channel2.basic_consume(
    queue='USA',
    on_message_callback=txt_callback
)


channel2.start_consuming()
"""

###############################################################################


class Consumer:
    def __init__(self, queue, callback):
        self.queue = queue
        self.callback = callback

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'))
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback
        )
        channel.start_consuming()
"""

"""
for el in consumer_list:
    Consumer(queue=el['country'], callback=el['callback'])
"""