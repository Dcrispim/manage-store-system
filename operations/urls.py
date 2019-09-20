from django.contrib import admin
from django.urls import path
from .views import home, salebuy

urlpatterns = [
    path('', home, name='home'),
    path('salebuy/', salebuy, name='salebuy'),

]