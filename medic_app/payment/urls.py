from django.urls import path
from . import views

urlpatterns = [
    path('/update_user_payment_method',views.update_user_payment_method),
    path('/get_user_payment_method_details',views.get_user_payment_method_details)
]