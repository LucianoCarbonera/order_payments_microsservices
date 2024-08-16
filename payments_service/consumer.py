import pika
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payments_service.settings')
django.setup()

from payments.models import Payment

def process_payment(ch, method, properties, body):
    try:
        payment_data = json.loads(body)
        order_id = payment_data['order_id']
        amount = payment_data['amount']

        payment = Payment.objects.create(
            order_id=order_id,
            amount=amount,
            status='PENDENTE'
        )
        print(f"Pagamento criado: {payment}")

        # Marca o pagamento como concluído
        payment.mark_as_completed()
        print(f"Pagamento {payment.transaction_id} concluído.")

        # Publica a mensagem no RabbitMQ para informar o orders_service sobre a atualização
        publish_status_update(order_id, 'COMPLETED')

    except Exception as e:
        print(f"Erro ao processar pagamento: {e}")

def publish_status_update(order_id, status):
    try:
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

        update_message = {
            'order_id': order_id,
            'status': status
        }

        channel.basic_publish(
            exchange='',
            routing_key=os.getenv('RABBITMQ_UPDATE_QUEUE', 'order_update_queue'),
            body=json.dumps(update_message)
        )

        connection.close()
        print(f"Mensagem de atualização de status enviada para o pedido {order_id}")

    except Exception as e:
        print(f"Erro ao enviar a atualização de status: {e}")

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

    # Garante que a fila 'order_queue' será criada
    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE', 'order_queue'))

    channel.basic_consume(
        queue=os.getenv('RABBITMQ_QUEUE', 'order_queue'),
        on_message_callback=process_payment,
        auto_ack=True
    )

    print("Aguardando mensagens. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
