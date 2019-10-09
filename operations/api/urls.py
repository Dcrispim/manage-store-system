from django.contrib import admin
from django.urls import path
from .views import SaleOrBuyRudView, SaleOrBuyListView

urlpatterns = [
    path('salebuy/<int:pk>',SaleOrBuyRudView.as_view(), name='api-salabuy'),
    path('salebuy/',SaleOrBuyListView.as_view(), name='api-salabuy'),


]