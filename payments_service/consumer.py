import pika
import os
import django
import json
import requests

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

        # Aqui marca como concluído o pagamento
        payment.mark_as_completed()
        print(f"Pagamento {payment.transaction_id} concluído.")

        # Envia a atualização de status para o serviço de pedidos
        update_order_status(order_id, 'COMPLETED')

    except Exception as e:
        print(f"Erro ao processar pagamento: {e}")

def update_order_status(order_id, status):
    try:
        url = f"http://localhost:8000/orders/update_status/{order_id}/"
        data = {'status': status}
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"Status do pedido {order_id} atualizado para {status}")
    except requests.exceptions.HTTPError as errh:
        print(f"Falha ao atualizar status do pedido {order_id} no serviço de pedidos: {errh}")
    except Exception as e:
        print(f"Erro ao enviar a atualização do status: {e}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    ))
    channel = connection.channel()

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
