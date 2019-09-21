from django.shortcuts import render, redirect

from .models import SalesOrBuy, Stock, Product, Client, CartItem
from .forms import SalesOrBuyForm

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
    list_prod = Product.objects.all()
    stock = Stock.objects.all()
    stock_list = []
    if input_cart and len(strToArrayObj(input_cart)[1])==0:
        list_t = strToArrayObj(input_cart)[0]
    else:
        errors.append('CartError: Empyt Cart')
        list_t = []
    

    def addCartItem(item, OPID):
        ID = Product.objects.get(pk=item['product'])
        IDSB = SalesOrBuy.objects.get(pk=OPID)
        CartItem.objects.create(product=ID, qtd=item['qtd'], opid=IDSB)   

    def updateStock(id,qtd):
        Stock.objects.filter(pk=id).update(qtd=qtd)

    def addCompra():
        for item in list_t:
            stockItem = Stock.objects.filter(product=item['product'])[0]
            qtd = stockItem.qtd+item['qtd']
            updateStock(stockItem.id, qtd)
            addCartItem(item, opid.id)
        return redirect('home')
    
    def addVenda():
        for item in list_t:
            stockItem = Stock.objects.filter(product=item['product'])[0]
            if stockItem.qtd<item['qtd']:
                errors.append('StockError: Insufficient stock quantity')
                return False
            qtd = stockItem.qtd-item['qtd']
            updateStock(stockItem.id, qtd)
            addCartItem(item, opid.id)
        return redirect('home')          
            

    if pesquisa != None:
        terms = pesquisa.split()
        lista = Prod.filter(name__icontains=pesquisa)

    for prod in list_prod:
        try:
            sti = stock.filter(product__exact=prod.pk)[0]
            if sti.qtd>0:
                stock_list.append(sti)
        except IndexError:
            pass
    print(form.is_valid())
    print(request.POST)
    if form.is_valid():
        
        try:
            if len(errors)==0:
                #opid = form.save()
                if form['mode'].value() == '0':
                    addVenda()
                elif form['mode'].value() == '1':
                    addCompra()
                   
        except Exception as erro:
           errors.append(erro)
        
        
            
    if errors:
        print(errors, 'ERROS')

    data = {
        'form': form,
        'stock': stock_list,
        'errors': errors
    }

    return render(request, 'salebuy.html', data)