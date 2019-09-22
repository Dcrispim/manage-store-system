let Parent = window.parent
let Frame = Parent.document.getElementById('div-popup')
let form = document.getElementById('form-add-client')
function closePopUp(){
    Frame.style.visibility='hidden'
}

function formSubmit(){
    form.submit()
    //closePopUp()
    Parent.location.reload()

}