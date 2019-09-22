let product = document.getElementById('prod_name')
let form = document.getElementById('main_form')

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

function submitForm() {
    setTimeout(()=>window.close(), 3000);
    form.submit()
   
    
}

window.addEventListener('onloadstart', product.value=getParam().prod_name.toUpperCase())