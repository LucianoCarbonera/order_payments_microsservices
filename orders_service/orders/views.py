from django.views.generic import CreateView
from django.http import HttpResponse
from .models import Order
import pika
import json
import os

def send_order_to_queue(order):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    ))
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE', 'order_queue'))

    order_data = {
        'order_id': order.id,
        'amount': str(order.price)
    }

    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('RABBITMQ_QUEUE', 'order_queue'),
        body=json.dumps(order_data)
    )

    connection.close()

class CreateOrderView(CreateView):
    model = Order
    fields = ['product_name', 'quantity', 'price']
    template_name = 'orders/order_form.html'
    success_url = '/orders/thanks/'

    def form_valid(self, form):
        response = super().form_valid(form)
        send_order_to_queue(self.object)
        return response

def home(request):
    return HttpResponse("Bem-vindo ao serviço de pedidos!")
