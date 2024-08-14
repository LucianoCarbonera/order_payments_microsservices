from django.urls import path
from .views import CreatePaymentView, PaymentsListView

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
    path('list/', PaymentsListView.as_view(), name='payments_list'),
]
