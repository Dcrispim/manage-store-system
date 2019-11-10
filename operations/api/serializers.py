from rest_framework import serializers
from operations.models import SalesOrBuy, CartItem, Product, Service, Operation, Client, Stock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        product = ProductSerializer(many=True, read_only=False)
        model = CartItem
        fields = [
            'product',
            'qtd',
            'op_type'
        ]


class SaleOrBuySerializer(serializers.ModelSerializer):
    cart_sb = CartItemSerializer(many=True)

    class Meta:
        model = SalesOrBuy
        fields = [
            'client',
            'mode',
            'status',
            'date',
            'off',
            'amount',
            "cart_sb"
        ]


class ServiceSerializer(serializers.ModelSerializer):
    cart_s = CartItemSerializer(many=True)

    class Meta:
        model = Service
        fields = [
            "description",
            "labor",
            "off",
            "amount",
            "client",
            "status",
            "date",
            "cart_s"
        ]



class OperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = '__all__'

