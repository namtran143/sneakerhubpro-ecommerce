from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment-success/<int:order_id>/', views.payment_success_view, name='payment_success'),
    path('orders/history/', views.order_history_view, name='order_history'),
]
