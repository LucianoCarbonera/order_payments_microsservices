from django.contrib import admin
from django.urls import path, include
from orders.views import home, thanks_view

urlpatterns = [
    path('', home, name='home'),  # Rota para a página inicial
    path('admin/', admin.site.urls),  # Rota para o admin do Django
    path('orders/', include('orders.urls')),  # Inclui as rotas do app orders
    path('orders/thanks/', thanks_view, name='thanks'),  # Rota para a página de agradecimento
]
