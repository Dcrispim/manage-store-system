if (localStorage.getItem('service')) {
    let service = localStorage.getItem('service')
}
else {
    localStorage.setItem('service', 'aberto')

}
let client = document.getElementById('client')
let date = document.getElementById('date')
let status = document.getElementById('status')
let cart = { 'items': [], 'materials': [] }
let ItemDoCaixa = null
let prod = document.getElementById('product')
let qtd = document.getElementById('qtd')
let total = { 'items': 0, 'materials': 0 }
let totalop = document.getElementById('totalop')
let totalopOff = document.getElementById('totalopOff')
let inputCart = [document.getElementById('input_items_cart'), document.getElementById('input_items_material')]
let form = document.getElementById('form-service')
let errors = []
let priceField = document.getElementById('sale_price')
let offService = document.getElementById('offService')
let BtnAddClient = document.getElementById('btn_add-client')
let popUpWindow = document.getElementById('iframe-popup')
var DivpopUpWindow = document.getElementById('div-popup')
let typeCartItem = ''
let labor = document.getElementById('labor')

let H = tamanho().h
let W = tamanho().w


function tamanho() {
    var x = document.body.scrollWidth || document.body.offsetWidth;
    var y = document.body.scrollHeight || document.body.offsetHeight;
    return { w: x, h: y };
}

function getErrors() {
    let divErrors = document.getElementById('div-errors').innerHTML
    divErrors = divErrors.replace('[', '').replace(']', '').split(';')
    if (divErrors.length > 0) {
        for (let i = 0; i < divErrors.length; i++) {
            let element = divErrors[i];
            if (element.length > 0) {
                errors.push(element)
            }

        }
    }
}

if (errors.length > 0) {
    for (let i = 0; i < errors.length; i++) {
        const erro = errors[i];
        if (erro.length > 0) {
            alert(erro)
        }

    }
}

function clearPesq() {
    prod.value = ''
    qtd.value = ''
}

function saveLostCart() {
    function save(e) {
        if (e) {
            if (e.value.length > 0) {
                localStorage.setItem(e.id, e.value || "")
            }
        }
    }
    save(client)
    save(date)
    save(status)
    save(labor)
    save(offService)

}

function recoveryLostCar() {
    function recovery(e) {
        if (e.tagName == 'SELECT') {
            e.selectedIndex = localStorage.getItem(e.id)

        } else if (e.value.length <= 0) {
            e.value = localStorage.getItem(e.id)
        }
    }

    recovery(client)
    recovery(date)
    recovery(status)
    recovery(labor)
    recovery(offService)

}

function setCart() {
    if (localStorage.getItem('cart') != null && localStorage.getItem('cart').length > 0) {
        let dbCart = `${localStorage.getItem('cart')}`
        let serviceCart = { items: JSON.parse(dbCart).items || [], 
            materials: JSON.parse(dbCart).materials || [] }
        cart = { ...serviceCart }
    }
    renderRows()
    setTotalOp()
}

function updateCartinput() {
    function updateCart(cart) {
        let selectCart = []
        cart.map(item => (
            selectCart.push({ "product": item.product[0], "qtd": item.qtd, "price": item.product[2] }
            )
        )
        )
        jsonCart = JSON.stringify(selectCart).substring(1, JSON.stringify(selectCart).length - 1)
        return jsonCart
    }

    inputCart[0].value = updateCart(cart.items)
    inputCart[1].value = updateCart(cart.materials)



}

function sendCartToLocalStorage() {
    jsonCart = JSON.stringify(cart)
    if (localStorage.cart) {
        dbCart = JSON.parse(localStorage.cart)   
    }else{
        dbCart = {}
    }
    dbCart['items'] = cart.items
    dbCart['materials'] = cart.materials
    localStorage.setItem('cart', JSON.stringify(dbCart))
}


function addCart() {
    let qtd = parseFloat(document.getElementById('qtd').value)
    let cartItem = document.getElementById('cart_item').checked
    let cartMaterials = document.getElementById('cart_material').checked
    if (ItemDoCaixa != null && qtd > 0) {
        if (cartItem) {
            cart.items.push({ product: ItemDoCaixa, qtd })
        } else if (cartMaterials) {
            cart.materials.push({ product: ItemDoCaixa, qtd })
        }
        renderRows()
        sendCartToLocalStorage()
        clearPesq()
        ItemDoCaixa = null

    }
    setTotalOp()
    localStorage.setItem('service', 'aberto')
}

function addToRegister(item) {
    prod.value = item[1]
    ItemDoCaixa = item
}

function setTotalOp() {
    totalop.value = ''
    totalopOff.value = ''
    desc = parseFloat(offService.value) / 100 || 0

    T = (total.items + total.materials + parseFloat(((labor.value || 0))))
    totalop.value = `${T.toFixed(2) || 0.00}`
    totalopOff.value = `${((T * (1 - desc)).toFixed(2)) || 0}`
    saveLostCart()
}

function removeCartItem(id, typeCart) {
    cart[typeCart].splice(id, 1)
    sendCartToLocalStorage()
    renderRows()
}

function renderRows() {
    total = { 'items': 0, 'materials': 0 }
    function setHead(title) {
        let head = `<thead class="thead-dark"><tr>`
        head += `<th scope="col">${title}</th>`
        head += `<th scope="col">Qtd/R$</th>`
        head += '<th scope="col">Act</th>'
        head += '</tr></thead>'
        return head
    }

    function render(typeCart, title = null) {
        let table = document.getElementById(`table_cart_${typeCart}`)
        title = title ? title : typeCart.charAt(0).toUpperCase() + typeCart.slice(1)
        table.innerHTML = setHead(title)
        for (let i = 0; i < cart[typeCart].length; i++) {
            let colProd = ` <td>${cart[typeCart][i].product[1]}</td>`
            let colQtdPrice = `<td>(${cart[typeCart][i].qtd})x R$ ${cart[typeCart][i].product[2]}</td>`
            let colAct = `<td><a class="btn btn-danger" onClick="removeCartItem(${i},'${typeCart}')"><i class="fa fa-trash-o"></i></a></td>`
            table.innerHTML += `<tr>${colProd}${colQtdPrice}${colAct}</tr>`
            total[typeCart] += (cart[typeCart][i].product[2] * cart[typeCart][i].qtd)

        }
    }

    render('items', 'Itens')
    render('materials', 'Materiais')

    setTotalOp()
    saveLostCart()
    updateCartinput()
    getErrors()
}

function openPopUp(route, w = 300, h = 200, data = []) {

    let left = (tamanho().w / 2)
    let top = (tamanho().h / 2)
    let param = ''
    for (let p = 0; p < data.length; p++) {
        const element = data[p];

        if (element.length >= 2 && element[1].length > 0) {
            param += `${element[0]}=${element[1]}`
        }
        if (p != data.length - 1) {
            param += '&'
        }
    }
    let URL = `${route}${param.length > 0 ? '?' + param : ``}`
    DivpopUpWindow.style.visibility = 'visible'
    popUpWindow.style.boxShadow = '2px 2px 8px';
    DivpopUpWindow.style.top = top + 'px'
    DivpopUpWindow.style.left = (left - (w / 2)) + 'px'
    popUpWindow.style.width = w + 'px'
    popUpWindow.style.height = h + 'px'
    popUpWindow.style.border = '0px';

    popUpWindow.setAttribute('src', URL)
}



function search() {
    let search = document.getElementById('search_form')
    search.submit()
}

function formSubmit() {
    localStorage.removeItem('cart')
    localStorage.removeItem('client')
    localStorage.removeItem('date')
    localStorage.removeItem('status')
    localStorage.setItem('service', 'fechada')
    localStorage.removeItem('off')
    let tempOff = parseFloat(offService.value)
    offService.value = tempOff/100
    if (parseFloat(labor.value) > 0) {
        let ok = confirm('Deseja Finalizar a service')
        if (ok == true) {
            form.submit()
        }
    } else {
        alert('Mão de obra não registrada')
    }
}
function getParam() {
    let query = location.search.slice(1);
    let partes = query.split('&');
    let data = {};
    partes.forEach(parte => {
        let chaveValor = parte.split('=');
        let chave = chaveValor[0];
        let valor = chaveValor[1];
        data[chave] = valor;
    });
    console.log(data)
    return data
}

function setCustomOff() {

    let newTotal = parseFloat(document.getElementById('totalopOff').value)
    let newOff = newTotal / parseFloat(totalop.value)
    if (newTotal < parseFloat(totalop.value)) {
        offService.value = ((1 - newOff) * 100).toFixed(2)
        setTotalOp()
    }
    document.getElementById('totalopOff').setAttribute('readonly',null)
    let newSubmitTotal = document.getElementById('submitNewTotal')
    let classSubmit = newSubmitTotal.getAttribute('class') + ' invisible'
    newSubmitTotal.setAttribute('class', classSubmit)
}

function activeTotalInput(){
    document.getElementById('totalopOff').removeAttribute('readonly')
    let newSubmitTotal = document.getElementById('submitNewTotal')
    let classSubmit = newSubmitTotal.getAttribute('class').replace('invisible','')
    newSubmitTotal.setAttribute('class', classSubmit)
}

window.addEventListener('load', () => {
    setCart()
    recoveryLostCar()
    renderRows()
    DivpopUpWindow.style.visibility = 'hidden'
    DivpopUpWindow.style.position = 'absolute'
    DivpopUpWindow.style.zIndex = 100

    BtnAddClient.setAttribute('onClick', "openPopUp('/addclient',300,300)")


})