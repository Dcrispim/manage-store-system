
let form = document.getElementById('op-form')
let formVisible = false

function showForm(){
    let tr = document.getElementById('tr-form')
    tr.style.visibility='visible'
    tr.style.position = 'relative'
    formVisible=true
}
function hideForm(){
    let tr = document.getElementById('tr-form')
    tr.style.visibility='hidden'
    tr.style.position = 'absolute'
    formVisible=false
}

function setForm(){
    if(formVisible){
        hideForm()
    }else{
        showForm()
    }
}


function opSubmit(){
    let credit = document.getElementById('ipt-credit')
    let debt = document.getElementById('ipt-debt')
    if(credit.value == ""){
        credit.value = 0
    }
    if(debt.value == ""){
        debt.value = 0
    }
    form.submit()
    
}


hideForm()