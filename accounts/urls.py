from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('users/', LandPage, name='land-page'),

    path('com-auth/', comanyRegister, name='com-register'),
    path('com-login/', companyLogin, name='com-login'),

    path('user-auth/', userRegister, name='user-register'),
    path('user-login/',userLogin, name='user-login')
]
