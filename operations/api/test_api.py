from os import system

import json
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
                'price':6
            }
        ]
 }

request = [
    "curl", 
    f'-d \'{sb}\'',
    "-X POST http://localhost:8000/api/salebuy/ -H'Authorization: Token 3013a1c5fbb66148dc801e0506e7554d0dde695b'", 
    "-H 'Content-Type: application/json'"
    ]
#print(f'-d "{sb}"'.translate(''))
c = f'ab'.translate(['a','b'])
system('curl -d \'{"client": 1, "mode": 0, "status": 1, "date": "2019-04-07", "off": "0.05", "amount": "70.00", "cart_sb": [{"product": 6, "qtd": 15, "price":20}]}\' -X POST http://localhost:8000/api/salebuy/ -H \'Authorization: Token 3013a1c5fbb66148dc801e0506e7554d0dde695b\' -H \'Content-Type: application/json\'')