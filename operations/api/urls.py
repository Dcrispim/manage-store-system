from django.contrib import admin
from django.urls import path
from .views import SaleOrBuyViewSet, ServiceViewSet, OperationViewSet, ProductViewSet, ClientViewSet, StockViewSet, SummaryViewSet




urlpatterns = [
    path('salebuy/<int:pk>',SaleOrBuyViewSet.as_view(), name='api-salebuy'),
    path('salebuy/',SaleOrBuyViewSet.as_view(), name='api-salebuy'),

    path('service/<int:pk>',ServiceViewSet.as_view(), name='api-service'),
    path('service/',ServiceViewSet.as_view(), name='api-service'),

    path('operation/<int:pk>',OperationViewSet.as_view(), name='api-operation'),
    path('operation/',OperationViewSet.as_view(), name='api-operation'),

    path('product/<int:pk>',ProductViewSet.as_view(), name='api-product'),
    path('product/',ProductViewSet.as_view(), name='api-product'),

    path('client/<int:pk>',ClientViewSet.as_view(), name='api-client'),
    path('client/',ClientViewSet.as_view(), name='api-client'),

    path('stock/<int:pk>',StockViewSet.as_view(), name='api-stock'),
    path('stock/',StockViewSet.as_view(), name='api-stock'),

    path('summary/',SummaryViewSet.as_view(), name='api-summary'),



]