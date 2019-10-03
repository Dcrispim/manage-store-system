if (localStorage.getItem('compra')) {
    let compra = localStorage.getItem('compra')

}
else {
    localStorage.setItem('compra', 'aberta')

}
let client = document.getElementById('client')
let date = document.getElementById('date')
let mode = document.getElementById('mode')
let status = document.getElementById('status')
let cart = []
let ItemDoCaixa = []
let prod = document.getElementById('product')
let qtd = document.getElementById('qtd')
let total = 0
let totalop = document.getElementById('totalop')
let totalopOff = document.getElementById('totalopOff')
let inputCart = document.getElementById('input_cart')
let form = document.getElementById('form-sale-buy')
let errors = []
let priceField = document.getElementById('sale_price')
let offSalebuy = document.getElementById('offSalebuy')
let AddClient
let AddProd
let BtnAddProd = document.getElementById('btn_add-prod')
let BtnAddClient = document.getElementById('btn_add-client')
let popUpWindow = document.getElementById('iframe-popup')
var DivpopUpWindow = document.getElementById('div-popup')

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
        if (e.value.length > 0) {
            localStorage.setItem(e.id, e.value)
        }
    }
    save(client)
    save(date)
    save(mode)
    save(status)
    save(offSalebuy)

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
    recovery(mode)
    recovery(status)
    recovery(offSalebuy)

}

function setCart() {
    if (localStorage.getItem('cart') != null && localStorage.getItem('cart').length > 0) {
        let dbCart = localStorage.getItem('cart')
        if (JSON.parse(dbCart).salebuy) {
            cart = [...JSON.parse(dbCart).salebuy]
        }

        //cart = [...] || []
    }

    renderRows()
    setTotalOp()
}

function updateCartinput() {
    let selectCart = []
    cart.map(item => (
        selectCart.push({ "product": item.product[0], "qtd": item.qtd, "price": item.product[2] }
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
    jsonCart = JSON.stringify({ 'salebuy': cart })
    localStorage.setItem('cart', jsonCart)
}

function setPriceField() {
    if (mode.value == 1) {
        priceField.removeAttribute('readOnly') 
        priceField.value=null
        priceField.setAttribute('required', true)
        initPrice = ItemDoCaixa[2] || ''
        priceField.value = initPrice
    } else if (mode.value == 0) {
        priceField.readOnly = true
        
    }
}

function addCart() {
    let qtd = parseFloat(document.getElementById('qtd').value)
    if (ItemDoCaixa != null && qtd > 0) {

        if (mode.value == 1) {
            price = parseFloat(priceField.value)
            cart.push({ product: [ItemDoCaixa[0], ItemDoCaixa[1], price], qtd })
        } else {
            cart.push({ product: ItemDoCaixa, qtd })
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
    qtd.value = 1
    qtd.focus()
    setPriceField()
}

function setTotalOp() {
    totalop.value = ''
    totalopOff.value = ''
    desc = parseFloat(offSalebuy.value) / 100 || 0
    totalop.value = `${total.toFixed(2)}`
    totalopOff.value = `${((total * (1 - desc))).toFixed(2)}`
    saveLostCart()
}

function removeCartItem(id) {
    cart.splice(id, 1)
    sendCartToLocalStorage()
    renderRows()
}

function renderRows() {
    total = 0
    function setHead(title) {
        let head = `<thead class="thead-dark"><tr>`
        head += `<th scope="col">${title}</th>`
        head += `<th scope="col">Qtd/R$</th>`
        head += '<th scope="col">Act</th>'
        head += '</tr></thead>'
        return head
    }
    let tableCart = document.getElementById('cart')
    tableCart.innerHTML = setHead('Produtos')
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

function openPopUp(route, w = 300, h = 200, data = []) {

    let left = (tamanho().w / 2)
    let top = (tamanho().h / 4)
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

function setCustomOff() {

    let newTotal = parseFloat(document.getElementById('totalopOff').value)
    let newOff = newTotal / parseFloat(totalop.value)
    if (newTotal < parseFloat(totalop.value)) {
        offSalebuy.value = ((1 - newOff) * 100).toFixed(2)
        setTotalOp()
        console.log('a')
    }
    document.getElementById('totalopOff').setAttribute('readonly', null)
    let newSubmitTotal = document.getElementById('submitNewTotal')
    let classSubmit = newSubmitTotal.getAttribute('class') + ' invisible'
    newSubmitTotal.setAttribute('class', classSubmit)
}

function activeTotalInput() {
    document.getElementById('totalopOff').removeAttribute('readonly')
    let newSubmitTotal = document.getElementById('submitNewTotal')
    let classSubmit = newSubmitTotal.getAttribute('class').replace('invisible', '')
    newSubmitTotal.setAttribute('class', classSubmit)
}

function verifyCart() {
    let err = false
    cart.forEach(item => {
        let qtd = parseFloat(item.qtd) || 0
        let price = parseFloat(item.product[2]) || 0
        if ((qtd <= 0) || (price <= 0)) {
            err = true
        }
    })
    return !err
}



function search() {
    let search = document.getElementById('search_form')
    search.submit()
}

function formSubmit() {
    localStorage.removeItem('cart')
    localStorage.removeItem('mode')
    localStorage.removeItem('client')
    localStorage.removeItem('date')
    localStorage.removeItem('status')
    localStorage.removeItem('offSalebuy')
    localStorage.setItem('compra', 'fechada')
    if (cart.length > 0) {
        if (verifyCart()) {

            let ok = confirm('Deseja Finalizar a compra')
            if (ok == true) {
                offSalebuy.value = parseFloat(offSalebuy.value) || 0
                form.submit()
            }
        }
            else {
                alert('ITEM SEM QUANTIDADE/PREÇO NO CARRINHO')
            }
        } else {
            alert('CARRINHO VAZIO')
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


mode.addEventListener('change', () => setPriceField())
window.addEventListener('load', () => {
    DivpopUpWindow.style.visibility = 'hidden'
    DivpopUpWindow.style.position = 'absolute'
    DivpopUpWindow.style.zIndex = 100

    BtnAddProd.setAttribute('onClick', "openPopUp('/addprod', 300,170, data=[['prod_name',document.getElementById('product').value]])")
    BtnAddClient.setAttribute('onClick', "openPopUp('/addclient',300,300)")

    document.getElementsByTagName('body')[0].style.height = '300px'
})