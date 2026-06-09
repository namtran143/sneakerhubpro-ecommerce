from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.product_manage_view, name='products'),
    path('products/add/', views.product_create_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_update_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),
    path('orders/', views.order_manage_view, name='orders'),
]
