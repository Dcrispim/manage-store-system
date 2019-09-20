if (localStorage.getItem('compra')) {
    let compra = localStorage.getItem('compra')
    if (compra != 'aberta') {
        localStorage.setItem('cart', [])
    }

} else {
    localStorage.setItem('compra', 'aberta')

}

let client = document.getElementById('id_client')
let date = document.getElementById('id_date')
let mode = document.getElementById('id_mode')
let status = document.getElementById('id_status')
let cart = []
let ItemDoCaixa = null
let prod = document.getElementById('product')
let qtd = document.getElementById('qtd')
let total = 0
let totalop = document.getElementById('totalop')
let inputCart = document.getElementById('input_cart')
let form = document.getElementById('main_form')
let errors = []
setCart()
setDateField(document.getElementById('id_date'))
recoveryLostCar()


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
        selectCart.push({"product": item.product[0], "qtd": item.qtd}
            )
        )
    )
    console.log(selectCart)
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

function setDateField(element){
    let = element.type = 'date'
}




function addCart() {
    let qtd = parseFloat(document.getElementById('qtd').value)
    if (ItemDoCaixa != null && qtd > 0) {
        cart.push({ product: ItemDoCaixa, qtd })
        renderRows()
        sendCartToLocalStorage()
        clearPesq()
        ItemDoCaixa = null


    }
    setTotalOp()
    localStorage.setItem('compra', 'aberta')
}

function addToRegister(item) {

    prod.value = item
    console.log(item)
    ItemDoCaixa = item
}

function setTotalOp() {
    console.log(total)
    totalop.innerHTML = ''
    totalop.innerText = `R$ ${total} `
    console.log(total)
}

function removeCartItem(id) {
    cart.splice(id, 1)
    sendCartToLocalStorage()
    renderRows()
}

function renderRows() {
    total=0
    var tableCart = document.getElementById('cart')
    tableCart.innerHTML = "<tr><th>Produto</th><th>QTD</th><th>ACT</th></tr>"
    for (let i = 0; i < cart.length; i++) {
        tableCart.innerHTML += `<tr> <td>${cart[i].product[1]}</td><td>(${cart[i].qtd})x R$ ${cart[i].product[2]}</td><td><a class="btn btn-danger" onClick="removeCartItem(${i})"><i class="fa fa-trash-o"></i></a></td></tr>`
        total += (cart[i].product[2] * cart[i].qtd)


    }
    console.log(total)

    setTotalOp()
    saveLostCart()
    updateCartinput()
    getErrors()
}

function formSubmit(){
    localStorage.removeItem('cart')
    localStorage.removeItem('id_mode')
    localStorage.removeItem('id_client')
    localStorage.removeItem('id_date')
    localStorage.removeItem('id_status')
    localStorage.setItem('compra','fechada')
    if(cart.length>0){
        form.submit()
    }else{
        alert('CARRINHO VAZIO')
    }
}
