from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls')),
    path('', include('django_prometheus.urls')),  # Adiciona a rota para métricas
]
