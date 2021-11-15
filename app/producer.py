import pika

from app import DEFAULT_INFO


def produce(data):
    with pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672)
    ) as connection:
        channel = connection.channel()
        for country in DEFAULT_INFO:
            channel.queue_declare(queue=country, durable=True)

        queue_name = data.country
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=data.xml_data,
            properties=pika.BasicProperties(  # could strengthen here
                delivery_mode=2,
            )
        )
