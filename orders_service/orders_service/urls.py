from django.contrib import admin
from django.urls import path, include
from orders.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
]
