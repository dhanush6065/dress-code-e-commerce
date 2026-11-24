from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]