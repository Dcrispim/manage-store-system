from rest_framework import generics, mixins

from operations.models import *
from .serializers import SaleOrBuySerializer, CartItemSerializer



# Create your views here.

class SaleOrBuyListView(generics.ListCreateAPIView):
    serializer_class = SaleOrBuySerializer
    
    def get_queryset(self):
        return SalesOrBuy.objects.all()


class SaleOrBuyRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    serializer_class = SaleOrBuySerializer
    
    def get_queryset(self):
        return SalesOrBuy.objects.all()


