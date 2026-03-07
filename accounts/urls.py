# ✅ FIXED — accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                                       views.login_view,          name='login'),
    path('logout/',                                views.logout_view,         name='logout'),
    path('register/',                              views.register_view,       name='register'),
    path('forgot-password/',                       views.forgot_password_view,name='forgot_password'),
    path('accounts/reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
    path('accounts/get-users/',                    views.get_users,           name='get_users'),
]