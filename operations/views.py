from django.shortcuts import render, redirect, HttpResponse
from django.db.utils import IntegrityError

from .models import SalesOrBuy, Stock, Product, Client, CartItem, Operation
from .forms import SalesOrBuyForm, ClientForm, ProductForm, ServiceForm

import json
from utils.parse import strToArrayObj
from utils.validate import prefixID as idValid
from .func import setProductStockList


# Create your views here.
def home(request):
    return render(request, 'home.html')


def salebuy(request):
    errors = []
    pesquisa = request.GET.get('product', None)
    form = SalesOrBuyForm(request.POST or None, )
    input_cart = request.POST.get('input_cart' or None)
    list_prod = []
    stock_list = []
    if input_cart and len(strToArrayObj(input_cart)[1]) == 0:
        list_cartitems = strToArrayObj(input_cart)[0]
    else:
        errors.append('CartError: Empyt Cart')
        list_cartitems = []

    def addOperation(item):
        Operation.objects.create(description=item['description'],
                                 orig_dest=item['orig_dest'], credit=item['credit'], debt=item['debt'],
                                 status=item['status'], date=item['date'],
                                 )

    def addCartItem(i, OPID):
        pkId = int(idValid(i['product'], 'P')) if idValid(
            i['product'], 'P') else i['product']
        ID = Product.objects.get(pk=pkId)
        IDSB = SalesOrBuy.objects.get(pk=OPID)
        CartItem.objects.create(product=ID, qtd=i['qtd'], opid=IDSB)

    def updateStock(id, qtd):
        Stock.objects.filter(pk=id).update(qtd=qtd)

    def addCompra(opId):
        total = 0
        for item in list_cartitems:
            pkId = int(idValid(item['product'], 'P')) if idValid(
                item['product'], 'P') else item['product']
            product_item = Product.objects.get(pk=pkId)

            if idValid(item['product'], 'P'):
                try:
                    Stock.objects.create(
                        product=product_item, qtd=item['qtd'], sale_price=item['price'])
                    total = total + item['qtd'] * item['price']
                except IntegrityError:
                    stockItem = Stock.objects.filter(product=product_item)[0]
                    qtd = stockItem.qtd+item['qtd']
                    updateStock(stockItem.id, qtd)
                    total = total + item['qtd'] * stockItem.sale_price
            else:
                stockItem = Stock.objects.filter(product=product_item)[0]
                qtd = stockItem.qtd+item['qtd']
                updateStock(stockItem.id, qtd)
                total = total + (item['qtd']*stockItem.sale_price)

            addCartItem(item, opid.id)
        return total

    def addVenda(opId):
        total = 0
        for item in list_cartitems:
            stockItem = Stock.objects.filter(product=item['product'])[0]
            if stockItem.qtd < item['qtd']:
                errors.append('StockError: Insufficient stock quantity')
                return False
            qtd = stockItem.qtd-item['qtd']
            updateStock(stockItem.id, qtd)
            addCartItem(item, opid.id)
            total = total + (stockItem.sale_price * item['qtd'])
        return total

    def setList():
        lp = setProductStockList(Stock,Product,pesquisa)
        if len(lp['errors'])==0:
            list_prod = lp['product']
            stock_list = lp['stock']
        else:
            errors.extend(lp['errors'])
        
    setList()

    if form.is_valid():
        try:
            if len(errors) == 0:
                opid = form.save()
                if form['mode'].value() == '0':
                    total = addVenda(opid)
                    addOperation({'description': f'IDV{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': total, 'debt': 0, 'status': opid.status, 'date': opid.date})

                elif form['mode'].value() == '1':
                    total = addCompra(opid)
                    addOperation({'description': f'IDC{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': 0, 'debt': total, 'status': opid.status, 'date': opid.date})
                setList()

        except KeyError as erro:
            errors.append(erro)
    print(request.POST.get('input_cart'))
    data = {
        'form': form,
        'stock': stock_list,
        'errors': errors,
        'products': list_prod}
    return render(request, 'salebuy.html', data)


def addClient(request):
    form = ClientForm(request.POST or None)

    if form.is_valid():
        form.save()
        return render(request, 'close.html')

    data = {
        'form': form
    }
    return render(request, 'addclient.html', data)

def addProduct(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return render(request, 'close.html')

    data = {
        'form': form
    }
    return render(request, 'addprod.html')

def service(request):
    errors = []
    pesquisa = request.GET.get('product' or None)
    list_prod  = []
    stock_list = []
    service_form = ServiceForm(request.POST or None)
    def setList():     
        lp = setProductStockList(Stock,Product,pesquisa)
        if len(lp['errors'])==0:
            list_prod.extend(lp['product'])
            stock_list.extend(lp['stock'])
        else:
            errors.extend(lp['errors'])
        
    setList()

    data = {
        'stock': stock_list,
        'products': list_prod,
        'form':service_form

    }
    print(request.POST)
    return render(request, 'service.html', data)

