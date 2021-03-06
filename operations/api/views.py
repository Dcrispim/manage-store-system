from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from operations.models import *
from .serializers import ( 
                            SaleOrBuySerializer,
                            CartItemSerializer, 
                            ProductSerializer, 
                            ServiceSerializer, 
                            OperationSerializer,
                            ClientSerializer,
                            StockSerializer
                        )

from .controler import valid_keys, validate_cart

import json


def __get_amount(cart, StockLock=True):
    amount = 0
    msg = []
    for item in cart:
        StockItem = Stock.objects.filter(product=item['product'])[0]
        amount += StockItem.sale_price*item['qtd']

        if StockLock and StockItem.qtd<item['qtd']:
            msg.append(f'{Stock.product.name}')
            return False, msg


def _setMultiplier(mult, value):
    query = Config.objects.filter(name=str(mult).lower())
    if len(query)>0:
        query.update(value=value)
        return True
    else:
        Config.objects.create(value_type=str(type(value)), value = str(value), name=mult )
        return True


def _getMultiplier(mult):
    
    try:
        v = Config.objects.filter(name=mult)[0]

        return float(v.value)

    except:
        _setMultiplier(mult,0)
        return 0 


# Create your views here.
class SaleOrBuyViewSet(APIView):
    serializer_class = SaleOrBuySerializer
    queryset = SalesOrBuy.objects.all()
    lookup_field = 'pk'

    def get(self, request, pk=None):
        
        if pk == None:
            salebuy = SalesOrBuy.objects.all()
            serializer = SaleOrBuySerializer(salebuy, many=True)
        else:
            try:
                salebuy = SalesOrBuy.objects.get(pk=pk)
                serializer = SaleOrBuySerializer(salebuy)
            except:
                return Response(404)

        return Response(serializer.data)
    
    @valid_keys(SaleOrBuySerializer().fields, ['id', 'amount'])
    @validate_cart('cart_sb', mode=1)
    def post(self, request, *args):
        from .controler import validate_SaleBuy as validate

        salebuy = SalesOrBuy.objects.all()
        valid = validate(request.data)
        if valid[0] or True:
            old_qtd = {}
            
            dt = request.data
            client = Client.objects.filter(pk=dt['client'])[0]
            

            item = SalesOrBuy.objects.create( client = client, date = dt['date'],
                                              mode = dt['mode'], status=dt['status'],
                                              off = dt['off'], amount = 0
                                              
                                            )
            
            amount = 0
            for i in dt['cart_sb']:
                product = Product.objects.filter(pk=i['product'])[0]
                CartItem.objects.create( product=product, 
                                         qtd=i['qtd'],
                                         sbid = item,
                                         op_type=0)
                
                
                stockItem = Stock.objects.get(product=i['product'])
                old_qtd[i['product']] = stockItem.qtd


                if dt['mode'] == 0:
                    new_qtd = stockItem.qtd - i['qtd'] 
                    Stock.objects.filter(product=i['product']).update(qtd=new_qtd)
                
                elif dt['mode'] == 1:

                    sale_price  = stockItem.sale_price
                    new_qtd     = stockItem.qtd + i['qtd']
                    mult        = float(1 + _getMultiplier('sale_price'))
                    rangeDiff   = float(1 + _getMultiplier('range'))

                    if float(i['price'])*mult > float(sale_price)*rangeDiff:
                        sale_price = float(i['price'])*mult
                    
                    Stock.objects.filter(product=i['product']).update(qtd=new_qtd, sale_price=sale_price)

                amount += Stock.objects.get(product=i['product']).sale_price*i['qtd']

            
            SalesOrBuy.objects.filter(pk=item.pk).update(amount=amount)
            
            description = f'IDC{item.pk}' if dt['mode']==1 else f'IDV{item.pk}'

            if dt['mode'] == 0:
                debt = 0
                credit = float(amount)
            elif dt['mode'] == 1:
                debt = float(amount)
                credit = 0

            op  = Operation.objects.create(
                                            description=description,
                                            orig_dest=client.name,
                                            credit=credit * (1 - float(dt['off'])),
                                            debt=debt * (1 - float(dt['off'])),
                                            status=dt["status"],
                                            date=dt["date"],
                                          )

            output = SaleOrBuySerializer(item).data
            output['response'] = {'status':200, 'msg':valid[1:]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1:]}
            return Response(output)


class ServiceViewSet(APIView):
    
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    lookup_field = 'pk'


    def get(self, request, pk=None):
        
        if pk == None:
            service = Service.objects.all()
            serializer = ServiceSerializer(service, many=True)
        else:
            try:
                service = Service.objects.get(pk=pk)
                serializer = ServiceSerializer(service)
            except:
                return Response(404)
        
        return Response(serializer.data)

    
    def post(self, request, *args):
        
        from .controler import validate_SaleBuy as validate

        dt = request.data
        valid = validate(request.data)
        

        if valid[0]:
            client = Client.objects.filter(pk=dt['client'])[0]
            old_qtd = {}
            amount = float(dt['labor'])
            svc = Service.objects.create(
                                            description = dt['description'],
                                            labor = dt['labor'],
                                            off = dt['off'],
                                            amount = amount,
                                            client = client,
                                            status = dt['status'],
                                            date = dt['date'],
                                        )


            for i in dt['cart_s']:
                product = Product.objects.filter(pk=i['product'])[0]
                CartItem.objects.create( product=product, 
                                         qtd=i['qtd'],
                                         svid = svc,
                                         op_type=i['op_type'])
                
                

                stockItem = Stock.objects.get(product=i['product'])

                old_qtd[i['product']] = stockItem.qtd
                new_qtd = stockItem.qtd - i['qtd']
                Stock.objects.filter(product=i['product']).update(qtd=new_qtd)

                amount += float(stockItem.sale_price)*float(i['qtd'])


            Service.objects.filter(pk=svc.pk).update(amount=amount)
            
            description = f'IDS{svc.pk}'
            op  = Operation.objects.create(
                                            description=description,
                                            orig_dest=client.name,
                                            credit=float(amount) * (1 - float(dt['off'])),
                                            debt=0,
                                            status=dt["status"],
                                            date=dt["date"],
                                          )
            
            output = ServiceSerializer(svc).data
            output['response'] = {'status':200, 'msg':valid[1:]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1:]}
            return Response(output)


class OperationViewSet(APIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    lookup_field = 'pk'


    def get(self, request, pk=None):
        
        if pk == None:
            operation = Operation.objects.all()
            serializer = OperationSerializer(operation, many=True)
        else:
            try:
                operation = Operation.objects.get(pk=pk)
                serializer = OperationSerializer(operation)
            except:
                return Response(404)

        
        return Response(serializer.data)

    
    def post(self, request, *args):

        from .controler import validate_SaleBuy as validate

        dt = request.data
        valid = validate(dt)
        if valid[0]:
            
            op  = Operation.objects.create(
                                            description=dt['description'],
                                            orig_dest=dt['orig_dest'],
                                            credit=dt['credit'],
                                            debt=dt['debt'],
                                            status=dt["status"],
                                            date=dt["date"],
                                          )

            output = request.data
            output['response'] = {'status':200, 'msg':valid[1:]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1:]}
            return Response(output)

class ProductViewSet(APIView):
    erializer_class = ServiceSerializer
    queryset = Service.objects.all()

    lookup_field = 'pk'

    def get(self, request, pk=None):
        
        if pk == None:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
        else:
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
            except:
                return Response(404)

        
        return Response(serializer.data)
    @valid_keys(ProductSerializer().fields, ['id'])
    def post(self, request, *args):
        
        
        dt = request.data
            
        prod  = Product.objects.create(
                                        name=dt['name'].upper(),
                                        brand=dt['brand'].upper(),
                                        unit=dt['unit'].upper(),
                                        )

        stock = Stock.objects.create(
                                        product=prod,
                                        qtd = 0, 
                                        sale_price=0,

                                    )

        output = ProductSerializer(prod).data
        
        output['response'] = {'status':200, 'msg':'Success'}
        print('Request Feita')
        return Response(output)


    @valid_keys(ProductSerializer().fields, ['id'])
    def put(self, request, pk):
        dt = request.data
        Product.objects.filter(pk=pk).update(
                                                name=dt['name'],
                                                brand=dt['brand'],
                                                unit=dt['unit'],
        )

class ClientViewSet(APIView):
    erializer_class = ServiceSerializer
    queryset = Service.objects.all()

    lookup_field = 'pk'
    def validate(self, data):
            msg = []
            try:
                name= data['name']
                email =  data['email']
                cell = data['cell']
                address = data['address']
                birth = data['birth']

                return True,['success']

            except KeyError as err:
                msg.append(f'Missing Key: {err}')
                return False, msg

    def get(self, request, pk=None):
        
        if pk == None:
            client = Client.objects.all()
            serializer = ClientSerializer(client, many=True)
        else:
            try:
                client = Client.objects.get(pk=pk)
                serializer = ClientSerializer(client)
            except:
                return Response(404)

        
        return Response(serializer.data)
    
    def post(self, request, *args):
           
        
        dt = request.data
        valid = self.validate(dt)
        if valid[0]:
            
            client  = Client.objects.create(
                                            name= dt['name'],
                                            email =  dt['email'],
                                            cell = dt['cell'],
                                            address = dt['address'],
                                            birth = dt['birth']
                                          )

            output = ClientSerializer(client).data
            output['response'] = {'status':200, 'msg':valid[1:]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1:]}
            return Response(output)


    def put(self, request, pk):
        valid = self.validate(request.data)
        dt = request.data
        if valid[0]:
            Client.objects.filter(pk=pk).update(
                                                    name= dt['name'],
                                                    email =  dt['email'],
                                                    cell = dt['cell'],
                                                    address = dt['address'],
                                                    birth = dt['birth']
            )


class StockViewSet(APIView):
    queryset = Stock.objects.all()

    lookup_field = 'pk'
    def validate(self, data):
            msg = []
            try:
                name= data['name']
                email =  data['email']
                cell = data['cell']
                address = data['address']
                birth = data['birth']

                return True,['success']

            except KeyError as err:
                msg.append(f'Missing Key: {err}')
                return False, msg

    def get(self, request, pk=None):
        
        if pk == None:
            stock = Stock.objects.all()
            serializer = StockSerializer(stock, many=True)
        else:
            try:
                stock = Stock.objects.get(pk=pk)
                serializer = StockSerializer(stock)
            except:
                return Response(404)

        
        return Response(serializer.data)






class SummaryViewSet(APIView):
    queryset = Operation.objects.all()

    lookup_field = 'pk'

    def get(self, request):
        output ={
                    'present':{
                                'pending':{
                                        'credit':87,
                                        'debt':850
                                },
                                'done':{
                                        'credit':706,
                                        'debt':850
                                },
                                'cancel':{
                                        'credit':706,
                                        'debt':850
                                }
                }
                    
                 }

        stock = Stock.objects.all()
        serializer = StockSerializer(stock, many=True)
        
        return Response(output)




