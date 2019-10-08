from django.shortcuts import render, redirect, HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import SalesOrBuy, Stock, Product, Client, CartItem, Operation, Service
from .forms import SalesOrBuyForm, ClientForm, ProductForm, ServiceForm, OperationForm

import json
from utils.parse import strToArrayObj, strToDate
from utils.validate import prefixID as idValid
from .func import setProductStockList


# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
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

    def addSBCartItem(i, OPID):
        '''
        i = {"product":Product(), "qtd":Float(), "price": Float()}
        '''

        if idValid(i['product'], 'P'):
            pkId = int(idValid(i['product'], 'P'))
        else:
            pkId = i['product']

        ID = Product.objects.get(pk=pkId)
        _addCartItem(pkId, i['qtd'], OPID, 0)

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

            addSBCartItem(item, opid.id)
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
            addSBCartItem(item, opid.id)
            total = total + (stockItem.sale_price * item['qtd'])
        return total

    def setList():
        lp = setProductStockList(Stock, Product, pesquisa)
        if len(lp['errors']) == 0:
            list_prod.extend(lp['product'])
            stock_list.extend(lp['stock'])
        else:
            errors.extend(lp['errors'])

    setList()
    print(request.POST)
    print(form.is_valid())
    if form.is_valid():
        try:
            if len(errors) == 0:
                opid = form.save()
                off = float(request.POST['off'])/100
                if form['mode'].value() == '0':
                    total = addVenda(opid)
                    _addOperation({'description': f'IDV{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': total, 'debt': 0, 'status': opid.status, 'date': opid.date, 'off': off})
                elif form['mode'].value() == '1':
                    total = addCompra(opid)
                    _addOperation({'description': f'IDC{ opid.pk }',
                                  'orig_dest': f'{opid.client}', 'credit': 0, 'debt': total, 'status': opid.status, 'date': opid.date, 'off': off})
                setList()
                return redirect('salebuy')
        except KeyError as erro:
            errors.append(erro)
    data = {
        'form': form,
        'stock': stock_list,
        'errors': errors,
        'products': list_prod}
    return render(request, 'salebuy.html', data)

@login_required
def addClient(request):
    form = ClientForm(request.POST or None)

    if form.is_valid():
        form.save()
        return render(request, 'close.html')

    data = {
        'form': form
    }
    return render(request, 'addclient.html', data)

@login_required
def addProduct(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return render(request, 'close.html')

    data = {
        'form': form
    }
    return render(request, 'addprod.html')

@login_required
def service(request):
    errors = []
    pesquisa = request.GET.get('product' or None)
    list_prod = []
    stock_list = []
    service_form = ServiceForm(request.POST or None)
    materials_cart = request.POST.get('input_materials_cart' or None)
    items_cart = request.POST.get('input_items_cart' or None)
    service_items = {'items':[], 'materials':[]}

    if materials_cart and len(strToArrayObj(materials_cart)[1]) == 0:
        service_items['materials'] = strToArrayObj(materials_cart)[0]
    else:
        list_cart_materials = []

    if items_cart and len(strToArrayObj(items_cart)[1]) == 0:
        service_items['items'] = strToArrayObj(items_cart)[0]
    else:
        list_cart_items = []

    def setList():
        lp = setProductStockList(Stock, Product, pesquisa)
        if len(lp['errors']) == 0:
            list_prod.extend(lp['product'])
            stock_list.extend(lp['stock'])
        else:
            errors.extend(lp['errors'])

    def addServiceItems(type_item, opid):
        totalitems = 0
        op_type = 1 if type_item=='items' else 2
        for item in service_items[type_item]:
            tp = 0 if type_item == 'items' else 1
            try:

                if _stockVerify(item['product'], item['qtd']):
                    prod = Product.objects.get(pk=item['product'])
                    stockItem = Stock.objects.filter(product=prod)[0]
                    if _stockSub(stockItem.pk, item['qtd']) > -1:
                        _addCartItem(item['product'],item['qtd'],opid.pk, op_type)
                        totalitems += stockItem.sale_price*item['qtd']
            except Exception as err:
                print(err)
                errors.append(err)
        return totalitems

    setList()
    print(request.POST)
    print(service_items)
    if service_form.is_valid():
        total = 0
        svId = service_form.save()
        total_items = addServiceItems('items', svId)
        total_materials = addServiceItems('materials', svId)
        total = total_items + total_materials + svId.labor
        print(total_items, total_materials, total)
        _addOperation({'description': f'IDS{ svId.pk }',
                      'orig_dest': f'{svId.client}',
                      'credit': total,
                      'debt': 0,
                      'status': svId.status,
                      'date': svId.date,
                      'off': svId.off})
        return redirect('service')

    data = {
        'stock': stock_list,
        'products': list_prod,
        'form': service_form

    }
    return render(request, 'service.html', data)

@login_required
def operation(request):
    form = OperationForm(request.POST or None)
    total_credits = 0
    total_debts = 0
    date_in = request.GET.get('date-in' or '')
    date_out = request.GET.get('date-out' or '')
    oprations = Operation.objects.all()
    try:
        list_op = oprations.filter(date__gte=date_in) if len(date_in)>0 else oprations
    except:
        list_op = oprations
    try:
        list_op = list_op.filter(date__lte=date_out) if len(date_out)>0 else list_op
    except:
        pass

    for op in list_op:
        total_credits += op.credit
        total_debts += op.debt


    if form.is_valid():
        form.save()
        return redirect('operation')
    data = {
        'form': form,
        'operations':list_op.order_by('-date'),
        'total_cred': total_credits,
        'total_deb': total_debts,
        'total': total_credits-total_debts
        }
    
    return render(request, 'operation.html', data)


def _addOperation(item):
    Operation.objects.create(description=item['description'],
                             orig_dest=item['orig_dest'], credit=float(item['credit'])*(1-float(item['off'])), debt=float(item['debt'])*(1-float(item['off'])),
                             status=item['status'], date=item['date'],
                             )


def _stockVerify(productId, qtd):
    product = Product.objects.get(pk=productId) if len(
        Product.objects.filter(pk=productId)) else None
    stockItem = Stock.objects.filter(product=product)[0] if len(
        Stock.objects.filter(product=product)) else None
    if product and stockItem and (stockItem.qtd >= qtd):
        return True
    else:
        return False


def _stockSub(stockId, qtd):
    stockItem = Stock.objects.get(pk=stockId)
    if stockItem.qtd < qtd:
        return -1
    else:
        new_qtd = stockItem.qtd-qtd
        Stock.objects.filter(pk=stockId).update(qtd=new_qtd)
        return new_qtd


def _addCartItem(prod_id, qtd, op_id, op_type):
    op_types = {0: 'COMPRA', 1: 'VENDA', 2: 'ITEM', 3: 'MATERIAL'}
    try:
        ID = Product.objects.get(pk=prod_id)
        if int(op_type) == 0:
            sb_id = SalesOrBuy.objects.get(pk=op_id)
            cart_item = CartItem.objects.create(
                product=ID, qtd=qtd, sbid=sb_id, op_type=op_type)
        elif 1 <= int(op_type) <= 2:
            sv_id = Service.objects.get(pk=op_id)
            cart_item = CartItem.objects.create(
                product=ID, qtd=qtd, svid=sv_id, op_type=op_type)

        return cart_item.pk
    except Exception as err:
        print(err)
        return -1

