let Parent = window.parent
let Frame = Parent.document.getElementById('div-popup')
let form = document.getElementById('form-add-client')
function closePopUp(){
    Frame.style.visibility='hidden'
}

function formSubmit(){
    form.submit()
    //closePopUp()

}

function Refresh(){
    Parent.console.log('1')
    Parent.location.href("/salebuy/Teste")
    Parent.console.log('2')
}