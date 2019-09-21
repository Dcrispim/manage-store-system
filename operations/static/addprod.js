let product = document.getElementById('prod_name')

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

window.addEventListener('onloadstart', product.value=getParam().prod_name.toUpperCase())