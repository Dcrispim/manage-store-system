from operations.models import *

def delete_data_tests(l=0):
    
    print('INICIANDO DELETE')
    delete_ids = Product.objects.filter(name__icontains='_TEST_')
    
    print('Aquivos de testes encontrados', len(delete_ids))
    
    for prod in delete_ids:
        print('\nTRYING DELETE PROD:',prod.id)
        print(Stock.objects.filter(product=prod).delete())
    
    print('VERIFICANDO REMANESCENTES')
    delete_ids = Product.objects.filter(name__icontains='_TEST_')
    print('Aquivos de testes encontrados', len(delete_ids))

    if len(delete_ids)>0 and l<10:
        print('\nREINICIANDO PROCESSO', l)
        l+=1
        return delete_data_tests(l)
    else:
        print('\nFINALIZADO')
        return delete_ids.delete()

delete_data_tests()