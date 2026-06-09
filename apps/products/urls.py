from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('review/add/<int:product_id>/', views.add_review_view, name='add_review'),
]
