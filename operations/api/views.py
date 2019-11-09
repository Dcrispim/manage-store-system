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
                            ClientSerializer
                        )



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
    
    def post(self, request, *args):
        def validate(data):
            msg = []
            try:
                client =  data['client']
                mode = data['mode']
                status = data['status']
                date = data['date']
                off = data['off']
                amount = data['amount']
                cart = data['cart_sb']
                cart['product']
                cart['qtd']
                if len(cart)<=0:
                    msg.append('Empty Cart')
                    return False, msg  
                tot = 0
                
                try:
                    
                    for item in cart:
                        StockItem = Stock.objects.filter(product=item['product'])[0]
                        tot += StockItem.sale_price*item['qtd']

                        if mode == 0 and StockItem.qtd<item['qtd']:
                            msg.append('Insufficient Sotck ')
                            return False, msg
                        

                
                    if float(tot) != float(amount):
                        msg.append('Amount Incorrect ')
                        return False, msg
                except:
                    msg.append('Missing Key')
                    return False, msg


                return True,msg

            except KeyError:
                msg.append('Missing Key')
                return False, msg

        salebuy = SalesOrBuy.objects.all()
        valid = validate(request.data)
        if valid[0]:
            old_qtd = {}
            
            dt = request.data
            client = Client.objects.filter(pk=dt['client'])[0]
            

            item = SalesOrBuy.objects.create( client = client, date = dt['date'],
                                              mode = dt['mode'], status=dt['status'],
                                              off = dt['off'], amount = dt['amount']
                                              
                                            )
            
            for i in dt['cart_sb']:
                product = Product.objects.filter(pk=i['product'])[0]
                CartItem.objects.create( product=product, 
                                         qtd=i['qtd'],
                                         sbid = item,
                                         op_type=0)
                
                

                stockItem = Stock.objects.get(product=i['product'])

                old_qtd[i['product']] = stockItem.qtd
                new_qtd = stockItem.qtd - i['qtd'] if dt['mode'] == 0 else stockItem.qtd + i['qtd']
                Stock.objects.filter(product=i['product']).update(qtd=new_qtd)

            
            description = f'IDC{item.pk}' if dt['mode']==1 else f'IDV{item.pk}'

            if dt['mode'] == 0:
                debt = 0
                credit = dt['amount']
            elif dt['mode'] == 1:
                debt = dt['amount']
                credit = 0

            op  = Operation.objects.create(
                                            description=description,
                                            orig_dest=client.name,
                                            credit=credit * (1 - float(dt['off'])),
                                            debt=debt * (1 - float(dt['off'])),
                                            status=dt["status"],
                                            date=dt["date"],
                                          )

            output = request.data
            output['id'] = svc.pk
            output['response'] = {'status':200, 'msg':valid[1]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1]}
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
        
        def validate(data):
            msg = []
            try:
                description= data['description']
                client =  data['client']
                labor = data['labor']
                status = data['status']
                date = data['date']
                off = data['off']
                amount = data['amount']
                cart = data['cart_s']


                tot = float(labor)
                
                try:
                    
                    for item in cart:
                        StockItem = Stock.objects.filter(product=item['product'])[0]
                        tot += float(StockItem.sale_price*item['qtd'])

                        if StockItem.qtd<item['qtd']:
                            print(StockItem.product, StockItem.qtd, item['qtd'])
                            msg.append(f'Insufficient Sotck: {item["product"]}')
                            return False, msg
                        

                
                    if float(tot) != float(amount):
                        msg.append('Amount Incorrect ')
                        return False, msg
                except Exception as err:
                    msg.append(f'{err}')
                    return False, msg


                return True,['success']

            except KeyError as err:
                msg.append(f'Missing Key: {err}')
                return False, msg

        dt = request.data
        valid = validate(request.data)
        

        if valid[0]:
            client = Client.objects.filter(pk=dt['client'])[0]
            old_qtd = {}
            svc = Service.objects.create(
                                            description = dt['description'],
                                            labor = dt['labor'],
                                            off = dt['off'],
                                            amount = dt['amount'],
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
            
            description = f'IDS{svc.pk}'
            op  = Operation.objects.create(
                                            description=description,
                                            orig_dest=client.name,
                                            credit=float(dt['amount']) * (1 - float(dt['off'])),
                                            debt=0,
                                            status=dt["status"],
                                            date=dt["date"],
                                          )
            
            output = request.data
            output['id'] = svc.pk
            output['response'] = {'status':200, 'msg':valid[1]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1]}
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

        def validate(data):
            msg = []
            try:
                description= data['description']
                orig_dest =  data['orig_dest']
                credit = data['credit']
                status = data['status']
                date = data['date']
                debt = data['debt']


                return True,['success']

            except KeyError as err:
                msg.append(f'Missing Key: {err}')
                return False, msg
        
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
            output['response'] = {'status':200, 'msg':valid[1]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1]}
            return Response(output)

class ProductViewSet(APIView):
    erializer_class = ServiceSerializer
    queryset = Service.objects.all()

    lookup_field = 'pk'
    def validate(self, data):
            msg = []
            try:
                name= data['name']
                brand =  data['brand']
                unit = data['unit']

                return True,['success']

            except KeyError as err:
                msg.append(f'Missing Key: {err}')
                return False, msg
            


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
    
    def post(self, request, *args):
        
        
        dt = request.data
        valid = self.validate(dt)
        if valid[0]:
            
            prod  = Product.objects.create(
                                            name=dt['name'],
                                            brand=dt['brand'],
                                            unit=dt['unit'],
                                          )

            output = request.data
            output['response'] = {'status':200, 'msg':valid[1]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1]}
            return Response(output)


    def put(self, request, pk):
        valid = self.validate(request.data)
        dt = request.data
        if valid[0]:
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

            output = request.data
            output['response'] = {'status':200, 'msg':valid[1]}
            return Response(output)
        else:
            output = request.data
            output['response'] = {'status':400, 'msg':valid[1]}
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