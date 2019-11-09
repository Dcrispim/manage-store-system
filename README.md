# manage-store-system

# Overview
This is a Django application based in a store that makes some service type  and sells products. The initial idea it's build a open source system that works in many differents enviroments.

# The API

## /api/product/
_Allowed methods: GET, POST, PUT_<br>
**Get**
```json
[
  {
  "id":1,
  "name": "Product 1",
  "brand": "Brand2",
  "unit": "Kg"
  },
  {
  "id":2,
  "name": "Product2",
  "brand": "Brand2",
  "unit": "Unit"
  }
]

```
**Post**
```json
{
  "name": "Product Name",
  "brand": "Product Brand",
  "unit": "Product Unit " // Kg, l, Unit
}
```

## /api/client/
_Allowed methods: GET, POST, PUT_<br>

**Get**
```json
[
    {
        "id": 1,
        "name": "Client 1",
        "cell": "9999999",
        "email": "client@client.com",
        "address": "Street anywhere",
        "birth": "2019-10-15"
    },
    {
        "id": 1,
        "name": "Client 2",
        "cell": "8888888",
        "email": "client2@client2.com",
        "address": "Street anyplace",
        "birth": "1987-07-94"
    }
 ]
```
**Post**
```json
{
        "name": "Client Name",
        "cell": "Client Cell",
        "email": "Client Email",
        "address": "Address Client",
        "birth": "2019-10-15"
 }
```

## /api/operation/
_Allowed methods: GET, POST_<br>
**Get**
```json
[
    {
        "id": 2,
        "description": "OP1",
        "orig_dest": "Client",
        "credit": "70.00",
        "debt": "0.00",
        "status": 1,
        "date": "2019-04-07"
    },
    {
        "id": 1,
        "description": "OP2",
        "orig_dest": "AnyStore",
        "credit": "0.00",
        "debt": "50.00",
        "status": 1,
        "date": "2019-5-06"
    }
 ]
```
**Post**
```json
{
        "description": "Operation Description",
        "orig_dest": "Origin or Destiny ",
        "credit": "7.00",
        "debt": "15.00",
        "status": 1, // 0='PENDDING' 1='OK' 2='CANCEL'
        "date": "2019-04-07"
}
```



## /api/salebuy/
_Allowed methods: GET, POST_<br>
**Get**
```json
[
    {
        "client": 1,
        "mode": 1,
        "status": 1,
        "date": "2019-04-07",
        "off": "0.05",
        "amount": "70.00",
        "cart_sb": [
            {
                "product": 1,
                "qtd": 1,
                "op_type": 0 //On 'salebuy' request is every equal 0
            },
            {
                "product": 3,
                "qtd": 1,
                "op_type": 0
            },
            {
                "product": 3,
                "qtd": 1,
                "op_type": 0
            },
            {
                "product": 4,
                "qtd": 1,
                "op_type": 0
            }
        ]
    },
     {
        "client": 1,
        "mode": 1,
        "status": 1,
        "date": "2019-04-07",
        "off": "0.00",
        "amount": "50.00",
        "cart_sb": [
            {
                "product": 2,
                "qtd": 5,
                "op_type": 0
            }
        ]
    }
 ]
```
**Post**
```json
{
        "client": 1, //Client ID
        "mode": 1, //0='SALE' 1='BUY'
        "status": 1, // 0='PENDDING' 1='OK' 2='CANCEL'
        "date": "2019-04-07",
        "off": "0.05",
        "amount": "70.00",
        "cart_sb": [
            {
                "product": 1, //Product ID
                "qtd": 1,
            },
            {
                "product": 3,
                "qtd": 1,
            },
            {
                "product": 3,
                "qtd": 1,
            },
            {
                "product": 4,
                "qtd": 1,
            }
        ]
 }
```
In the post request, the item is created in the **SalesOrBuy** table, a **CartItem** for each item in _"cart_sb"_, an **Operation** and **Stock** table update.

If there is not enough stock for sale, the request will be canceled.

## /api/service/
_Allowed methods: GET, POST_<br>
**Get**
```json
[
    {
        "description": "Some Service",
        "labor": "50.00",
        "off": "0.0000",
        "amount": "70.00",
        "client": 1,
        "status": 1,
        "date": "2019-11-09",
        "cart_s": [
            {
                "product": 1,
                "qtd": 1,
                "op_type": 2
            },
            {
                "product": 3,
                "qtd": 1,
                "op_type": 1
            }
        ]
    },
    {
        "description": "Othe Service",
        "labor": "50.00",
        "off": "0.0000",
        "amount": "70.00",
        "client": 1,
        "status": 1,
        "date": "2019-11-09",
        "cart_s": []
    }
 ]
```
**Post**
```json
{
        "description": "Description of Service",
        "labor": "50.00",
        "off": "0.0000",
        "amount": "70.00",
        "client": 1, //Client ID
        "status": 1, // 0='PENDDING' 1='OK' 2='CANCEL'
        "date": "2019-11-09",
        "cart_s": [
            {
                "product": 1,
                "qtd": 1,
                "op_type": 2 // 1='ITEM' 1='OK' 2='MATERIAL'
            }
        ]
 }
```

In the post request, the item is created in the **Service** table, a **CartItem** for each item in _"cart_s"_, an **Operation** and **Stock** table update.

If there is not enough stock for Item or Matereial, the request will be canceled.


# _The application_ (In rebuilding process)

## 1.1 Sales and Buys
Each Sales and Buy contains:<br>
**Client**: Default it's an Anonymous register that may included. It's a necessary field and is not possible write a name which not registered. But the Register is easy gone using the side button the field
<br>
**Mode**: It's a choice field "Sale" or "Buy". If you mark as Buy the **Price** field will be editable else you mark as "Sale" the price will be the price registered on database
<br>
**Status**: It's a choice field "Pending", "Cancel" or "OK"
<br>
**Date**: Date of operation
<br>
**Off**: Percent value discount of operation. Default is 0
<br>
**Cart**: The cart contains every product chosen with yours quantity and price
<br><br>
**Search Field**:<br>
You can write any words for search a product or choose from below list.
<br>
**Qtd**: After choice product, type it the quantity
<br>
**Price**: Product's price.

When you Buy a product, his **Sale price** will be multiplied for a constant registered on database table "**Config**" as "sale_price" automatically. Default value of sale_price constant is 0;
<br>
Ex:
```
sale_price Constant = 0,2(20%)

Product: Apple
Price: 1
```
on database
```
Product: Apple
Sale_Price: 1,2
```

