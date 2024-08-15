from django.urls import path
from .views import CreateOrderView, update_order_status  # Importa as views necessárias

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('update_status/<int:order_id>/', update_order_status, name='update_order_status'),  # Rota para atualizar o status do pedido
]
