from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]