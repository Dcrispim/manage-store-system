from django.contrib import admin
from django.urls import path
from .views import home, salebuy, addProduct, addClient, service

urlpatterns = [
    path('', home, name='home'),
    path('salebuy/', salebuy, name='salebuy'),
    path('addclient/', addClient, name='addclient'),
    path('addprod/', addProduct, name='addprod'),
    path('service/', service, name='service'),



]