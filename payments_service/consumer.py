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

        payment.mark_as_completed()
        print(f"Pagamento {payment.transaction_id} concluído.")

    except Exception as e:
        print(f"Erro ao processar pagamento: {e}")

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
