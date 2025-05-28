from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('/create_new_user',views.create_new_user)
]
