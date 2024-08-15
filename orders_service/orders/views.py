from django.views.generic import CreateView
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order
from .producer import publish_message

class CreateOrderView(CreateView):
    model = Order
    fields = ['product_name', 'quantity', 'price']
    template_name = 'orders/order_form.html'
    success_url = '/orders/thanks/'  # URL de redirecionamento após a criação do pedido

    def form_valid(self, form):
        response = super().form_valid(form)
        # Verifica se o objeto está salvo antes de acessar o ID
        order = self.object
        publish_message({
            'order_id': order.pk,  # Usar `pk` para obter o ID do pedido
            'amount': str(order.price)
        })
        return response

def home(request):
    return render(request, 'orders/home.html')

def thanks_view(request):
    # Pega o último pedido criado para exibir na página de agradecimento
    order = Order.objects.latest('order_id')
    return render(request, 'orders/thanks.html', {'order': order})

@csrf_exempt  # Desabilita a verificação de CSRF para esta view
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(pk=order_id)
            data = json.loads(request.body)
            order.status = data['status']
            order.save()
            return JsonResponse({'message': 'Status atualizado com sucesso'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Pedido não encontrado'}, status=404)
    return JsonResponse({'error': 'Método não permitido'}, status=405)
