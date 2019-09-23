def setProductStockList(Stock, Product, query_filter=None, HARD=True):
    __UNIQUE_CTRL_LIST__ = []
    stock = Stock.objects.all()
    lp = Product.objects.all()
    errors = []
    list_product = []
    list_stock = []
    query_list = []

    if query_filter != None:
        if HARD == False:
            terms = query_filter.split()
        else:
            terms = [query_filter]
        for term in terms:
            query_list.extend(lp.filter(name__icontains=term))
    else:
        query_list.extend(lp)

    for prod in query_list:
        try:
            stock_itemQ = stock.filter(product__exact=prod.pk)
            stock_item = stock_itemQ[0] if stock_itemQ else None
            n_stock_prod = stock_item.product.name if stock_itemQ else None

            if stock_itemQ and stock_item not in list_stock and n_stock_prod not in __UNIQUE_CTRL_LIST__:
                list_stock.append(stock_item)
                __UNIQUE_CTRL_LIST__.append(n_stock_prod)
            elif prod not in list_product and prod.name not in __UNIQUE_CTRL_LIST__:
                list_product.append(prod)
                __UNIQUE_CTRL_LIST__.append(prod.name)
        except IndexError as err:
            errors.append(err)
    
    return {'stock': list_stock, 'product': list_product, 'errors': errors}
