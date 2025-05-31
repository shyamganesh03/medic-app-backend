from django.urls import path
from . import views

urlpatterns = [
    path('/get_user_details',views.get_user_details),
    path('/update_user_details',views.update_user_details)
]
