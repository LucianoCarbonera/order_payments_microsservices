import pika
import json
import os

def publish_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    ))
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE', 'order_queue'))

    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('RABBITMQ_QUEUE', 'order_queue'),
        body=json.dumps(message)
    )
    connection.close()
