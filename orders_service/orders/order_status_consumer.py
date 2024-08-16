import sys
import os
import django
import json
import pika

# Adicionar o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_service.settings')

# Inicializar o Django
django.setup()

from orders.models import Order

def update_order_status(ch, method, properties, body):
    try:
        update_data = json.loads(body)
        order_id = update_data['order_id']
        status = update_data['status']

        order = Order.objects.get(pk=order_id)
        order.status = status
        order.save()

        print(f"Status do pedido {order_id} atualizado para {status}")

    except Order.DoesNotExist:
        print(f"Pedido {order_id} não encontrado.")
    except Exception as e:
        print(f"Erro ao atualizar o status do pedido {order_id}: {e}")

def main():
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

    # Garante que a fila 'order_update_queue' será criada
    channel.queue_declare(queue=os.getenv('RABBITMQ_UPDATE_QUEUE', 'order_update_queue'))

    channel.basic_consume(
        queue=os.getenv('RABBITMQ_UPDATE_QUEUE', 'order_update_queue'),
        on_message_callback=update_order_status,
        auto_ack=True
    )

    print("Aguardando mensagens para atualização de status. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
