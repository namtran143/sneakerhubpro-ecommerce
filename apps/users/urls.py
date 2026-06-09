from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.auth_view, name='login'),
    path('register/', views.auth_view, name='register'),
    path('auth/', views.auth_view, name='auth'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
