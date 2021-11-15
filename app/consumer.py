import pika

from app.db_requests import save_data_to_db
from app.files_requests import save_data_to_file
from app import DEFAULT_INFO


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

for country in DEFAULT_INFO:
    channel.queue_declare(queue=country, durable=True)


def db_callback(ch, method, properties, body):
    save_data_to_db(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def txt_callback(ch, method, properties, body):
    save_data_to_file(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)  # can improve in 2 part of tutorial to messages not to stack


channel.basic_consume(
    queue='Ukraine',
    on_message_callback=db_callback
)
channel.basic_consume(
    queue='UK',
    on_message_callback=db_callback
)
channel.basic_consume(
    queue='Italy',
    on_message_callback=txt_callback
)
channel.basic_consume(
    queue='China',
    on_message_callback=txt_callback
)
channel.basic_consume(
    queue='USA',
    on_message_callback=txt_callback
)


channel.start_consuming()
