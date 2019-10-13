# manage-store-system

# Overview
This is a Django application based in a store that makes some service type  and sells products. The initial idea it's build a open source system that works in many differents enviroments.

**disclaimer**<br>
The application it's begins in production in a small store. So, the frontend currently is's build em pure HTML, but when the RestAPI have been done the frontend will be migrate to React JS. Therefore some funcionalitys maybe not build as pretty as it should

# The application

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

