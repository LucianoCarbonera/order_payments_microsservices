import pika
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_service.settings')
django.setup()

from orders.models import Order

def update_order_status(ch, method, properties, body):
    try:
        data = json.loads(body)
        order_id = data['order_id']
        status = data['status']

        order = Order.objects.get(order_id=order_id)
        order.status = status
        order.save()
        print(f"Status do pedido {order_id} atualizado para {status}")
    except Order.DoesNotExist:
        print(f"Pedido {order_id} não encontrado")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    ))
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE_UPDATE', 'order_update_queue'))

    channel.basic_consume(
        queue=os.getenv('RABBITMQ_QUEUE_UPDATE', 'order_update_queue'),
        on_message_callback=update_order_status,
        auto_ack=True
    )

    print("Aguardando mensagens para atualização de status. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
