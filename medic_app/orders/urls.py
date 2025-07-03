from django.urls import path
from . import views

urlpatterns = [
    path('/create_orders',views.create_order),
    path('/get_order_details',views.get_order_details),
    path('/get_order_payment_details',views.get_order_payment_details),
    path('/revoke_order',views.revoke_order),
    path('/get_user_order_details',views.get_user_order_details),
    
]