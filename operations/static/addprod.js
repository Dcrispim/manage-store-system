let Parent = window.parent
let product = document.getElementById('prod_name')

let pesc = window.parent.document.getElementById('product').value

function getParam(){
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

function closePopUp(){
    window.parent.document.getElementById('div-popup').style.visibility='hidden'
}

window.addEventListener('load', ()=>{
    product.value=pesc.toUpperCase()
    console.log(Parent.document.getElementById('product').value)
})
