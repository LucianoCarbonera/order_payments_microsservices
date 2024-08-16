import pika
import json
import os


def publish_message(message):
    # Estabelecendo a conexão com RabbitMQ utilizando variáveis de ambiente
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        virtual_host=os.getenv('RABBITMQ_VHOST', '/'),
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_DEFAULT_USER', 'guest'),
            password=os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
        )
    ))

    channel = connection.channel()

    # Declarando a fila
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE', 'order_queue'))

    # Publicando a mensagem na fila
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('RABBITMQ_QUEUE', 'order_queue'),
        body=json.dumps(message)
    )

    connection.close()
