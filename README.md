# manage-store-system

# Overview
This is a Django application based in a store that makes some service type  and sells products. The initial idea it's build a open source system that works in many differents enviroments.

**disclaimer**<br>
The application it's begins in production in a small store. So, the frontend currently is's build em pure HTML, but when the RestAPI have been done the frontend will be migrate to React JS. Therefore some funcionalitys maybe not build as pretty as it should

# The application

## 1.1 Sales and Buys
Each Sales and Buy contains:<br>
**Client**: Default it's an Anonymous register that may included. It's a necessary field and is not possible write a name which not registered. But the Register is easy gone using the side button the field
<br><br>
**Mode**: It's a choice field "Sale" or "Buy". If you mark as Buy the **Price** field will be editable else you mark as "Sale" the price will be the price registered on database. It's a necessary field
<br><br>
**Status**: It's a choice field and the default it's "Pending", "OK" and "Canceled".It's a necessary field
<br><br>
 