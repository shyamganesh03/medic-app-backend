from django.urls import path
from . import views

urlpatterns = [
    path('/get_categories_list',views.get_categories_list),
    path('/get_product_list',views.get_product_list),
    path('/get_product_list_by_category_id',views.get_product_list_by_category_id),
    path('/add_products_bulk',views.add_products_bulk),
    path('/get_product_details_by_id',views.get_product_details_by_id)
]