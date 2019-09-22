from django.forms import ModelForm
from .models import SalesOrBuy, Stock, Product, Client, CartItem


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