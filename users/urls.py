from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('categories/', views.categories, name='categories'),
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-signup-otp/', views.resend_signup_otp, name='resend_signup_otp'),
    path('login/', views.customer_login, name='login'),
    path('logout/', views.customer_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-otp/', views.reset_password_otp, name='reset_password_otp'),
    path('resend-password-reset-otp/', views.resend_password_reset_otp, name='resend_password_reset_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('profile/', views.customer_profile, name='profile'),
    path('my-addresses/', views.my_addresses, name='my_addresses'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email'),
    path('verify-new-email/', views.verify_new_email, name='verify_new_email'),
    path('add-address/', views.add_address, name='add_address'),
    path(
    'edit-address/<int:address_id>/',
    views.edit_address,
    name='edit_address'
    ),
    path(
    'delete-address/<int:address_id>/',
    views.delete_address,
    name='delete_address'
    ),
    path(
    'set-default-address/<int:address_id>/',
    views.set_default_address,
    name='set_default_address'
    ),
    
]