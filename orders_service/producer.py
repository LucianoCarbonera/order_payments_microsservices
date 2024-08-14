import pika
import json
import os


def publish_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))

    channel.basic_publish(exchange='',
                          routing_key=os.getenv('RABBITMQ_QUEUE'),
                          body=json.dumps(message))
    connection.close()
