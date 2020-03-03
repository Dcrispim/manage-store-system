from operations.models import *
from os import system
cont = 0
def delete_data_tests(l=0):
    
    print('INICIANDO DELETE')
    delete_ids = Product.objects.filter(name__icontains='_TEST_')
    cont = delete_ids
    print('Aquivos de testes encontrados', len(delete_ids))
    
    for prod in delete_ids:
        print('\nTRYING DELETE PROD:',prod.id)
        Stock.objects.filter(product=prod).delete()
    
    print('VERIFICANDO REMANESCENTES')
    print('Aquivos de testes encontrados', len(Product.objects.filter(name__icontains='_TEST_')))
    return delete_ids.delete()
    print('\nFINALIZADO')

delete_data_tests()
if cont!=0:
    system('python3 manage.py shell -c"from operations.delete import *"')