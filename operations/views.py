from django.shortcuts import render, redirect, HttpResponse
from django.db.utils import IntegrityError

from .models import SalesOrBuy, Stock, Product, Client, CartItem, Operation
from .forms import SalesOrBuyForm, ClientForm, ProductForm

import json
from utils.parse import strToArrayObj


# Create your views here.
def home(request):
    return render(request, 'home.html')


def salebuy(request):
    errors = []
    pesquisa = request.GET.get('product', None)
    form = SalesOrBuyForm(request.POST or None, )
    input_cart = request.POST.get('input_cart' or None)
    list_prod = []
    stock = Stock.objects.all()
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

    def addCartItem(item, OPID):
        if str(item['product'])[0].upper() == 'P':
            ID = Product.objects.get(pk=int(item['product'][1:]))
        else:
            ID = Product.objects.get(pk=item['product'])
        IDSB = SalesOrBuy.objects.get(pk=OPID)
        CartItem.objects.create(product=ID, qtd=item['qtd'], opid=IDSB)

    def updateStock(id, qtd):
        Stock.objects.filter(pk=id).update(qtd=qtd)

    def addCompra(opId):
        total = 0
        for item in list_cartitems:
            new_prod = False
            if str(item['product'])[0].upper() == 'P':
                new_prod = True
                product_item = Product.objects.get(pk=int(item['product'][1:]))
            else:
                product_item = item['product']

            if new_prod:
                try:
                    Stock.objects.create(
                        product=product_item, qtd=item['qtd'], sale_price=item['price'])
                    total = total + item['qtd']*item['price']
                except IntegrityError:
                    stockItem = Stock.objects.filter(product=product_item)[0]
                    qtd = stockItem.qtd+item['qtd']
                    updateStock(stockItem.id, qtd)
                    total = total + item['qtd']*stockItem.sale_price
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
        __UNIQUE_CTRL_LIST__ = []
        lp = Product.objects.all()
        list_prod.clear
        stock_list.clear
        if pesquisa != None:
            terms = pesquisa.split()
            lista = lp.filter(name__icontains=pesquisa)
        else:
            lista = lp

        for prod in lista:
            try:
                sti = stock.filter(product__exact=prod.pk)
                if sti and sti[0] not in stock_list and sti[0].product.name not in __UNIQUE_CTRL_LIST__:
                    stock_list.append(sti[0])
                    __UNIQUE_CTRL_LIST__.append(sti[0].product.name)
                elif prod not in list_prod and prod.name not in __UNIQUE_CTRL_LIST__:
                    list_prod.append(prod)
                    __UNIQUE_CTRL_LIST__.append(prod.name)
            except IndexError as err:
                errors.append(err)
    setList()
    print(form.is_valid())
    print(request.POST)
    if form.is_valid():
        try:
            if len(errors) == 0:
                opid = form.save()
                if form['mode'].value() == '0':
                    total = addVenda(opid)
                    addOperation({'description': f'IDV{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': total, 'debt': 0 , 'status': opid.status, 'date': opid.date})
    
                elif form['mode'].value() == '1':
                    total = addCompra(opid)
                    addOperation({'description': f'IDC{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': 0, 'debt': total, 'status': opid.status, 'date': opid.date})
                setList()

        except KeyError as erro:
            print('ERRO', erro)
            errors.append(erro)

    data = {
        'form': form,
        'stock': stock_list,
        'errors': errors,
        'products': list_prod}
    return render(request, 'salebuy.html', data)


def addClient(request):
    form = ClientForm(request.POST or None)

    print(form.is_valid())
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
