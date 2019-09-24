from django.forms import ModelForm
from .models import SalesOrBuy, Stock, Product, Client, CartItem, Service


class SalesOrBuyForm(ModelForm):
    
    class Meta:
        model = SalesOrBuy
        fields = (
            'client',
            'mode',
            'status',
            'date',
             )

class ClientForm(ModelForm):
    
    class Meta:
        model = Client
        fields = (
            'name',
            'cell',
            'email',
            'address',
            'birth'
             )

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = (
            'name',
            'brand',
            'unit',
             )

class ServiceForm(ModelForm):
    
    class Meta:
        model = Service
        fields = (
            'description',
            'itens',
            'material',
            'labor',
            'off',
            'client',
            'status',
            'date'
             )