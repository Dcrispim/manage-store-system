from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

STATUS_CHOICES = [
    (0, 'PENDENTE'),
    (1, 'OK'),
    (2, 'CANCELADO'),
]

class Product(models.Model):

    name    = models.CharField(max_length=100)
    brand   = models.CharField(max_length=50)
    unit    = models.CharField(max_length=50, default='UNIDADE')

    def __str__(self):
        return self.name


class Client(models.Model):
    name    = models.CharField(max_length=100)
    cell    = models.CharField(max_length=20)
    email   = models.CharField(max_length=150)
    address = models.CharField(max_length=100, null = False)
    birth   = models.DateField(auto_now=False, auto_now_add=False, null = False)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    qtd = models.IntegerField( default=0, validators=[ MinValueValidator(0)] )
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.product.name


class SalesOrBuy(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    mode   = models.IntegerField(choices = [(0,'VENDA'), (1,'COMPRA')])
    status = models.IntegerField(choices = STATUS_CHOICES, default='PENDENTE')
    date   = models.DateField(auto_now=False, auto_now_add=False)
    off   = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=8, default=0, decimal_places=2)


    def __str__(self):
        mode = 'VENDA' if self.mode==0 else 'COMPRA'
        return str(f'{self.pk} - {self.client} - ({mode})')

class Service(models.Model):
    description = models.CharField(max_length=100)
    labor       = models.DecimalField(max_digits=8, decimal_places=2)
    off         = models.DecimalField(max_digits=5, null=True, default=0, decimal_places=4)
    amount      = models.DecimalField(max_digits=8, default=0, decimal_places=2)
    client      = models.ForeignKey(Client, null=True, on_delete=models.PROTECT)
    status      = models.IntegerField(choices = STATUS_CHOICES, default='PENDENTE')
    date        = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.description

class CartItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)
    qtd = models.IntegerField( default=0, validators=[ MinValueValidator(0) ] )
    sbid = models.ForeignKey(SalesOrBuy, null=True, blank=True, on_delete=models.CASCADE, related_name="cart_sb")
    svid = models.ForeignKey(Service, null=True, blank=True ,on_delete=models.CASCADE, related_name="cart_s")
    op_type = models.IntegerField(choices = [(0,'COMPVEND'), (1,'ITEM'), (2,'MATERIAL')], default=0)

    def __str__(self):
        if self.svid == None and self.sbid != None:
            ID = self.sbid.pk
        elif self.svid != None and self.sbid == None:
            ID = self.svid.pk
        else:
            mode = 'ERRO'
            ID = 0

        mode = {0:'COMPVEND', 1:'Service-ITEM', 2:'Servce-MATERIAL'}
        return str(f'({mode[self.op_type]}:{ID}) {self.product.name}')




class Operation(models.Model):
    description = models.CharField(max_length=100)
    orig_dest = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    debt = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.IntegerField(choices = STATUS_CHOICES, default='PENDENTE')
    date   = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.description

class Config(models.Model):
    value_type = models.CharField(max_length=10, default="float")
    name = models.CharField(max_length=30)
    value = models.TextField(blank=True, null=True)


    
