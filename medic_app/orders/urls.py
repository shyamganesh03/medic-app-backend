from django.urls import path
from . import views

urlpatterns = [
    path('/create_orders',views.create_order),
    path('/get_order_details',views.get_order_details)
]