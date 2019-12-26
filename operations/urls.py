from django.contrib import admin
from django.urls import path
from .views import (home,
                    salebuy,
                    addProduct,
                    addClient,
                    service,
                    operation,
                    listSaleBuy,
                    detailSaleBuy,
                    listService)

urlpatterns = [
    path('', home, name='home'),
    path('salebuy/list/', listSaleBuy, name='list_salebuy'),
    path('service/list/', listService, name='list_service'),
    path('salebuy/<int:pk>/', detailSaleBuy, name='list_salebuy'),
    path('salebuy/', salebuy, name='salebuy'),
    path('addclient/', addClient, name='addclient'),
    path('addprod/', addProduct, name='addprod'),
    path('service/', service, name='service'),
    path('operation/', operation, name='operation'),
    


]