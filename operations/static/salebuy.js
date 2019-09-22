if (localStorage.getItem('compra')) {
    let compra = localStorage.getItem('compra')
    if (compra != 'aberta') {
        localStorage.setItem('cart', [])
    }

} 
else {
    localStorage.setItem('compra', 'aberta')

}
let client = document.getElementById('client')
let date = document.getElementById('date')
let mode = document.getElementById('mode')
let status = document.getElementById('status')
let cart = []
let ItemDoCaixa = null
let prod = document.getElementById('product')
let qtd = document.getElementById('qtd')
let total = 0
let totalop = document.getElementById('totalop')
let totalopOff = document.getElementById('totalopOff')
let inputCart = document.getElementById('input_cart')
let form = document.getElementById('main_form')
let errors = []
let priceField = document.getElementById('sale_price')
let off = document.getElementById('off')
let H = tamanho().h
let W = tamanho().w

setCart()
recoveryLostCar()
setPriceField()

function tamanho() {
    var x = document.body.scrollWidth || document.body.offsetWidth;
    var y = document.body.scrollHeight || document.body.offsetHeight;
    return { w: x, h: y };
}

function getErrors(){
    let divErrors = document.getElementById('div-errors').innerHTML
    divErrors = divErrors.replace('[','').replace(']','').split(';')
    if(divErrors.length>0){
        for (let i = 0; i < divErrors.length; i++) {
            let element = divErrors[i];
            if(element.length>0){
                errors.push(element)
            }
            
        }
    }
}

if(errors.length>0){
    for (let i = 0; i < errors.length; i++) {
        const erro = errors[i];
        if (erro.length>0) {
            alert(erro)
        }
        
    }
}

function clearPesq() {
    prod.value = ''
    qtd.value = ''
}

function saveLostCart(){
    function save( e ) {
        if(e.value.length > 0 ){
            localStorage.setItem(e.id, e.value)
        }
    }
    save(client)
    save(date)
    save(mode)
    save(status) 

}

function recoveryLostCar(){
    function recovery(e){
        if (e.tagName =='SELECT'){
            e.selectedIndex = localStorage.getItem(e.id)

        } else if(e.value.length <= 0 ){
            e.value = localStorage.getItem(e.id)
        }
    }

    recovery(client)
    recovery(date)
    recovery(mode)
    recovery(status)

}

function setCart() {
    if (localStorage.getItem('cart') != null && localStorage.getItem('cart').length > 0) {
        let dbCart = localStorage.getItem('cart')
        let db = dbCart.split('},')
        for (let i = 0; i < db.length; i++) {
            if (i < db.length - 1) {
                cart.push(JSON.parse(db[i] + '}'))
            } else {
                cart.push(JSON.parse(db[i]))
            }
        }
    }

    renderRows()
    setTotalOp()
}

function updateCartinput(){
    let selectCart = [] 
    cart.map(item => (
        selectCart.push({"product": item.product[0], "qtd": item.qtd, "price":item.product[2]}
            )
        )
    )

    jsonCart = JSON.stringify(selectCart).substring(1, JSON.stringify(selectCart).length - 1)

    inputCart.value = jsonCart

}

function sendCartToLocalStorage() {
    if (localStorage.getItem('cart')) {
        localStorage.removeItem('cart')
    }
    jsonCart = JSON.stringify(cart).substring(1, JSON.stringify(cart).length - 1)
    localStorage.setItem('cart', jsonCart)
}

function setPriceField(){
    if (mode.value == 1){
        priceField.style.visibility = 'visible'
        priceField.setAttribute('required',true)
        initPrice = ItemDoCaixa[2] | ''
        priceField.value = initPrice
    } else if (mode.value == 0){
        priceField.style.visibility = 'hidden'
    }
}

function addCart() {
    let qtd = parseFloat(document.getElementById('qtd').value)
    if (ItemDoCaixa != null && qtd > 0) {
        
        if(mode.value==1){
            price = parseFloat(priceField.value)
            cart.push({product:[ItemDoCaixa[0],ItemDoCaixa[1], price], qtd})
        }else{
            cart.push({ product: ItemDoCaixa, qtd})
        }
        renderRows()
        sendCartToLocalStorage()
        clearPesq()
        ItemDoCaixa = null

    }
    setTotalOp()
    localStorage.setItem('compra', 'aberta')
}

function addToRegister(item) {
    prod.value = item[1]
    ItemDoCaixa = item
    setPriceField()
}

function setTotalOp() {
    totalop.innerHTML = ''
    totalopOff.innerHTML = ''
    desc = parseFloat(off.value)/100 || 0
    totalop.innerText = `R$ ${total.toFixed(2)} `
    totalopOff.innerText = `R$ ${((total*(1-desc))).toFixed(2)} `
}

function removeCartItem(id) {
    cart.splice(id, 1)
    sendCartToLocalStorage()
    renderRows()
}

function renderRows() {
    total=0
    let tableCart = document.getElementById('cart')
    tableCart.innerHTML = "<tr><th>Produto</th><th>QTD</th><th>ACT</th></tr>"
    for (let i = 0; i < cart.length; i++) {
        let colProd = ` <td>${cart[i].product[1]}</td>`
        let colQtdPrice = `<td>(${cart[i].qtd})x R$ ${cart[i].product[2]}</td>`
        let colAct = `<td><a class="btn btn-danger" onClick="removeCartItem(${i})"><i class="fa fa-trash-o"></i></a></td>`
        tableCart.innerHTML += `<tr>${colProd}${colQtdPrice}${colAct}</tr>`
        total += (cart[i].product[2] * cart[i].qtd)


    }
    setTotalOp()
    saveLostCart()
    updateCartinput()
    getErrors()
}

function openPopUp(route, w=300, h=200, data=[]){
    
    let left = (tamanho().w/2)
    let top = (tamanho().h/2)
    let param = ''
    for (let p = 0; p < data.length; p++) {
        const element = data[p];
        
        if(element.length>=2 && element[1].length>0){
            param += `${element[0]}=${element[1]}`
        }
        if(p!= data.length-1){
            param+='&'
        } 
    }

    window.open(`${route}${param.length>0? '?'+param :``}`, "MsgWindow", `width=${w},height=${h},left=${left},top=${top}`)
}

function search(){
    let search = document.getElementById('search_form')
    search.submit()
}

function formSubmit(){
    localStorage.removeItem('cart')
    localStorage.removeItem('mode')
    localStorage.removeItem('client')
    localStorage.removeItem('date')
    localStorage.removeItem('status')
    localStorage.setItem('compra','fechada')
    if(cart.length>0){
        let ok = confirm('Deseja Finalizar a compra')
        if(ok==true){
            form.submit()
        }
    }else{
        alert('CARRINHO VAZIO')
    }
}
mode.addEventListener('change', ()=>setPriceField())