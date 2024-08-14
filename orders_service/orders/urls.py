from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
]
