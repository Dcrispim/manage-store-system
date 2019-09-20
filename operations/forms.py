from django.forms import ModelForm
from .models import SalesOrBuy


class SalesOrBuyForm(ModelForm):
    
    class Meta:
        model = SalesOrBuy
        fields = (
            'client',
            'mode',
            'status',
            'date',
             )