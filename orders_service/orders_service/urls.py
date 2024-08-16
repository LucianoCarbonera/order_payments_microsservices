from django.contrib import admin
from django.urls import path, include
from orders.views import home, thanks_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('orders/', include('orders.urls')),  # Inclui as rotas do app orders
    path('orders/thanks/', thanks_view, name='thanks'),  # Adiciona a rota para a página de agradecimento
    path('', include('django_prometheus.urls')),  # Adiciona a rota para métricas
]
