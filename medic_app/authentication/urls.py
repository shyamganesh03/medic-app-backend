from django.urls import path
from . import views

urlpatterns = [
    path('/create_new_user',views.create_new_user),
    path('/delete_user',views.delete_authenticated_user)
]
