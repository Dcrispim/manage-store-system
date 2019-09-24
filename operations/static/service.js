if (localStorage.getItem('service')) {
    let service = localStorage.getItem('service')
    if (service != 'aberto') {
        localStorage.setItem('cart', {})
    }

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
let off = document.getElementById('off')
let BtnAddClient = document.getElementById('btn_add-client')
let popUpWindow = document.getElementById('iframe-popup')
var DivpopUpWindow = document.getElementById('div-popup')
let typeCartItem = ''

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

}

function setCart() {
    if (localStorage.getItem('cart') != null && localStorage.getItem('cart').length > 0) {
        let dbCart = `${localStorage.getItem('cart')}`
        cart = { ...JSON.parse(dbCart) }
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
    if (localStorage.getItem('cart')) {
        localStorage.removeItem('cart')
    }
    jsonCart = JSON.stringify(cart)
    localStorage.setItem('cart', jsonCart)
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
    totalop.innerHTML = ''
    totalopOff.innerHTML = ''
    desc = parseFloat(off.value) / 100 || 0

    T = (total.items + total.materials + parseFloat(((labor.value || 0))))
    totalop.innerText = `R$ ${T.toFixed(2) || 0.00} `
    totalopOff.innerText = `R$ ${((T * (1 - desc)).toFixed(2)) || 0} `
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


window.addEventListener('load', () => {
    setCart()
    recoveryLostCar()
    renderRows()
    DivpopUpWindow.style.visibility = 'hidden'
    DivpopUpWindow.style.position = 'absolute'
    DivpopUpWindow.style.zIndex = 100

    BtnAddClient.setAttribute('onClick', "openPopUp('/addclient',300,300)")


})