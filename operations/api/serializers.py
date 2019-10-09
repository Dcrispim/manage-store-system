from rest_framework import serializers
from operations.models import SalesOrBuy

class SaleOrBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrBuy
        fields = [
            'client',
            'mode',
            'status',
            'date',
            'off',
            'amount'
        ]



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrBuy
        fields = [
            'product',
            'qtd',
            'sbid',
            'svid',
            'op_type',
        ]