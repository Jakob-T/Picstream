from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('verify/', views.verify_user, name='verify_user'),
    path('login_user/',views.login_user, name='login_user'),
    path('regular_login/', views.regular_login, name='regular_login'),
    path('profile/', views.user_profile, name='profile'),
    path('moralis_auth', views.moralis_auth, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('verify_message', views.verify_message, name='verify_message'),
    path('moralis_profile', views.moralis_profile, name='moralis_profile'),
]
