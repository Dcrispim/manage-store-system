from operations.models import Stock
from operations.api.serializers import *
from rest_framework.response import Response

def validate_keys(fields, data, exclude=[]):
    for key in fields:
        if key not in data.keys() and key not in exclude:
            return False, key,'validate_keys'
    return True, 'success','validate_keys'



def vk(fields, exclude: list =[])-> tuple([bool,str, str]):
    def validate(data: dict):
        for key in fields:
            if key not in data.keys() and key not in exclude:
                return False, key,'validate_keys'
        

def teste(fields, exclude=[]):
    def inner_test(func_validate):
        def ii(data):
            for key in fields:
                if key not in data.keys() and key not in exclude:
                    return False, key
            return func_validate(data) #func, param_inner, param_decorator
        return ii

    return inner_test


def valid_keys(fields, exclude=[]):
    def inner_test(func_validate):
        def validate_keys( self, request, *arg):
            for key in fields:
                if key not in request.data.keys() and key not in exclude:
                    return Response({'status':400, 'msg':f"'{key}' missing"})
            return func_validate(self, request, *arg) #func, param_inner, param_decorator
        return validate_keys

    return inner_test


def validate_cart(cart, product='product', qtd='qtd', **conditions):
    temp_keys ={}

    def inner_test(func_validate):
        def _validate_cart(self, request, *arg):
            for k in conditions.keys():
                if request.data[k]!= conditions[k]:
                    return func_validate(self, request,*arg)
            try:
                for item in request.data[cart]:
                   
                    subtotal = 0
                    #verifica se o item já foi consultado e faz a consulta da soma
                    if item[product] in temp_keys.keys():
                        subtotal += temp_keys[item[product]]
                        temp_keys[item[product]] += item[qtd]
                    else:
                        temp_keys[item[product]] = item[qtd]

                    vstk = verify_Stock(item[product],item[qtd]+subtotal)
                    if vstk[0] == False:
                        return Response({'status':400, 'msg':f"{item[qtd]+subtotal} {item[product]} requestded but only {vstk[1]} on Stock"})
                    
                    

                return func_validate(self, request,*arg)

            except KeyError as k:

                return Response({'status':400, 'msg':f"missing {k}"})
            
            except KeyError as e:
                return Response({'status':400, 'msg':f"{e}"})

        return _validate_cart


    return inner_test



















@teste(OperationSerializer().fields,['id'])
def strText(data):
    return '-'.join(data)

def verify_Stock(itemID, qtd):
    StockItem = Stock.objects.filter(product=itemID)
    if len(StockItem)==0:
        return False, f'{itemID} NOT FAUND','verify_Stock'
    stk_qtd = StockItem[0].qtd
    if stk_qtd <qtd:
        return False, stk_qtd,'verify_Stock'
    return True, stk_qtd,'verify_Stock'

def validat_cart(cart, product='product', qtd='qtd', **conditions):
    temp_keys ={}
    try:

        for item in cart:
            
            for k in conditions.keys():
                try:
                    if item[k]!=conditions[k]:
                        return True,'validate_cart 1'
                except KeyError as k:
                    return False, k ,'validate_cart 2'
            
            subtotal = 0
            #verifica se o item já foi consultado e faz a consulta da soma
            if item[product] in temp_keys.keys():
                subtotal += temp_keys[item[product]]
                temp_keys[item[product]] += item[qtd]
            else:
                temp_keys[item[product]] = item[qtd]

            vstk = verify_Stock(item[product],item[qtd]+subtotal)
            if vstk[0] == False:
                return False, (item[product],vstk[1]),'validate_cart 3'
            
            

        return True,0

    except KeyError as k:

        return False, f'{k} not found','validate_cart 4'
    
    except KeyError as e:
        return False, e,'validate_cart 5'
    

s = {
        "description": "Some Service",
        "labor": "50.00",
        "off": "0.0000",
        "amount": "70.00",
        "client": 1,
        "status": 1,
        "date": "2019-11-09",
        "cart_s": [
            {
                "product": 6,
                "qtd": 1,
                "op_type": 2
            },
            {
                "product": 6,
                "qtd": 1,
                "op_type": 1
            }
        ]
    }

@teste(SaleOrBuySerializer().fields,['id','amount'])
def validate_SaleBuy(data):
    err = []
    #verifica se é uma compra [1] ou venda [0] 
    if int(data['mode'])!=1:
        return True,0,'validate_SaleBuy 2'

    #verifica se há estoque para todos os items do carrinho
    vcart = validate_cart(data['cart_sb'])
    if vcart[0]==False:
        err.append(vcart[1:])
        return False, err,'validate_SaleBuy 3'
    

    if len(err)==0:
        return True,0,'validate_SaleBuy 4'


def validate_Service(data):
    err = []
    #verifica se tem todos os campos
    vk = validate_keys(ServiceSerializer().fields, data,['id', 'amount'])
    if vk[0]==False:
        err.append(vk[1])
        return False,err,'validate_Service 1'

    #verifica se é uma compra [1] ou venda [0] 

    #verifica se há estoque para todos os items do carrinho
    vcart = validate_cart(data['cart_s'])
    if vcart[0]==False:
        err.append(vcart[1:])
        return False, err,'validate_Service 3'
    

    if len(err)==0:
        return True,0,'validate_Service 4'

@teste(OperationSerializer().fields,['id'])
def validate_Operation(data):
    err = []

    if len(err)==0:
        return True,0,'validate_Operation 4'
op ={
        "description": "Operation Description",
        "orig_dest": "Origin or Destiny ",
        "credit": "7.00",
        "debt": "15.00",
        "status": 1,
        "date": "2019-04-07"
}

sb = {
        "client": 1, 
        "mode": 1, 
        "status": 1, 
        "date": "2019-04-07",
        "off": "0.05",
        "amount": "70.00",
        "cart_sb": [
            {
                "product": 6,
                "qtd": 1,
            }
        ]
 }

#print(OperationSerializer().validate(op))
print(validate_SaleBuy(s))

#curl -X GET http://localhost:8000/api/product/ -H 'Authorization: Token 3013a1c5fbb66148dc801e0506e7554d0dde695b'